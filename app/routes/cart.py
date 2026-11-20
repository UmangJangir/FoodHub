from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.models import Cart
from app.services.cart_service import (
    add_to_cart,
    update_cart_item,
    remove_cart_item
)

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart"
)


@cart_bp.route("/")
@login_required
def view_cart():

    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()

    return render_template(
        "cart.html",
        cart=cart
    )


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add(product_id):

    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        flash("Invalid quantity.", "danger")
        return redirect(url_for("products.product_detail", product_id=product_id))

    success, message = add_to_cart(
        current_user.id,
        product_id,
        quantity
    )

    flash(message, "success" if success else "danger")

    if success:
        return redirect(url_for("cart.view_cart"))

    return redirect(url_for("products.product_detail", product_id=product_id))


@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update(item_id):

    try:
        quantity = int(request.form.get("quantity", 1))
    except (ValueError, TypeError):
        flash("Invalid quantity.", "danger")
        return redirect(url_for("cart.view_cart"))

    success, message = update_cart_item(
        current_user.id,
        item_id,
        quantity
    )

    flash(message, "success" if success else "danger")

    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove(item_id):

    success, message = remove_cart_item(
        current_user.id,
        item_id
    )

    flash(message, "success" if success else "danger")

    return redirect(url_for("cart.view_cart"))
