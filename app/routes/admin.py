
import os
from functools import wraps
from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, abort, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import User, Product, Order


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Admin-only access
def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped


# Dashboard
@admin_bp.route("/")
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_customers = User.query.filter_by(role="customer").count()

    revenue = db.session.query(
        db.func.coalesce(db.func.sum(Order.total_amount), 0)
    ).filter(
        Order.payment_status.in_(["paid", "completed"])
    ).scalar()

    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_customers=total_customers,
        revenue=revenue,
        recent_orders=recent_orders
    )


# Products
@admin_bp.route("/products")
@admin_required
def products():
    all_products = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "admin/products.html",
        products=all_products
    )


# Add product
@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        try:
            price = Decimal(request.form.get("price", "0"))
            stock = int(request.form.get("stock", "0"))
        except (InvalidOperation, ValueError):
            flash("Please enter a valid price and stock.", "danger")
            return render_template("admin/product_form.html", product=None)

        if not name or not category or price <= 0 or stock < 0:
            flash("Please enter valid product details.", "danger")
            return render_template("admin/product_form.html", product=None)

        image = request.files.get("image")
        image_filename = None

        if image and image.filename:
            filename = secure_filename(image.filename)
            extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

            if extension not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                flash("Only PNG, JPG, JPEG and WEBP images are allowed.", "danger")
                return render_template("admin/product_form.html", product=None)

            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)

            image_filename = filename
            image.save(os.path.join(upload_folder, image_filename))

        product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock,
            image_filename=image_filename,
            is_available=True
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=None)


# Edit product
@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        try:
            price = Decimal(request.form.get("price", "0"))
            stock = int(request.form.get("stock", "0"))
        except (InvalidOperation, ValueError):
            flash("Please enter a valid price and stock.", "danger")
            return render_template("admin/product_form.html", product=product)

        if not name or not category or price <= 0 or stock < 0:
            flash("Please enter valid product details.", "danger")
            return render_template("admin/product_form.html", product=product)

        product.name = name
        product.category = category
        product.description = description
        product.price = price
        product.stock = stock
        product.is_available = request.form.get("is_available") == "on"

        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)
            extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

            if extension not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                flash("Only PNG, JPG, JPEG and WEBP images are allowed.", "danger")
                return render_template("admin/product_form.html", product=product)

            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)

            image.save(os.path.join(upload_folder, filename))
            product.image_filename = filename

        db.session.commit()

        flash("Product updated successfully!", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=product)


# Disable / enable product without deleting order history
@admin_bp.route("/products/<int:product_id>/toggle", methods=["POST"])
@admin_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_available = not product.is_available

    db.session.commit()

    flash("Product availability updated.", "success")
    return redirect(url_for("admin.products"))


# Orders
@admin_bp.route("/orders")
@admin_required
def orders():
    all_orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin/orders.html",
        orders=all_orders
    )


@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)

    allowed_statuses = {
        "placed",
        "confirmed",
        "preparing",
        "out_for_delivery",
        "delivered",
        "cancelled"
    }

    new_status = request.form.get("order_status", "").strip()

    if new_status not in allowed_statuses:
        flash("Invalid order status.", "danger")
        return redirect(url_for("admin.orders"))

    order.order_status = new_status
    db.session.commit()

    flash("Order status updated successfully.", "success")
    return redirect(url_for("admin.orders"))


# Customers
@admin_bp.route("/customers")
@admin_required
def customers():
    all_customers = User.query.filter_by(
        role="customer"
    ).order_by(User.created_at.desc()).all()

    return render_template(
        "admin/customers.html",
        customers=all_customers
    )
