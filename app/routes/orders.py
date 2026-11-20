from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.order_service import place_order
from app.models import Order

orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():

    if request.method == "POST":

        delivery_address = request.form.get("delivery_address", "").strip()
        phone = request.form.get("phone", "").strip()
        payment_method = request.form.get("payment_method", "COD")

        if len(phone) > 15 or not phone.isdigit():
            flash("Please enter a valid phone number.", "danger")
            return render_template("checkout.html")

        success, message = place_order(
            current_user.id,
            delivery_address,
            phone,
            payment_method
        )

        flash(message, "success" if success else "danger")

        if success:
            return redirect(url_for("orders.my_orders"))

    return render_template("checkout.html")


@orders_bp.route("/my-orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).order_by(Order.created_at.desc()).all()

    return render_template(
        "my_orders.html",
        orders=orders
    )


@orders_bp.route("/<int:order_id>")
@login_required
def order_detail(order_id):

    order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "order_detail.html",
        order=order
    )
