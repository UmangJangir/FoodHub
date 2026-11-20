from decimal import Decimal

from app.extensions import db
from app.models import Cart, Order, OrderItem


def place_order(user_id, delivery_address, phone, payment_method="COD"):

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart or not cart.items:
        return False, "Your cart is empty."

    if not delivery_address.strip():
        return False, "Please enter your delivery address."

    if not phone.strip():
        return False, "Please enter your phone number."

    if payment_method != "COD":
        return False, "Currently, only Cash on Delivery is supported."

    total_amount = Decimal("0.00")

    for item in cart.items:
        product = item.product

        if not product or not product.is_available:
            return False, "A product in your cart is unavailable."

        if item.quantity < 1 or item.quantity > product.stock:
            return False, f"Insufficient stock for {product.name}."

        total_amount += Decimal(str(product.price)) * item.quantity

    try:
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            payment_method="COD",
            payment_status="pending",
            order_status="placed",
            delivery_address=delivery_address.strip(),
            phone=phone.strip()
        )

        db.session.add(order)
        db.session.flush()

        for item in cart.items:
            product = item.product

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                quantity=item.quantity
            )

            db.session.add(order_item)

            product.stock -= item.quantity

        db.session.delete(cart)
        db.session.commit()

        return True, f"Order #{order.id} placed successfully!"

    except Exception:
        db.session.rollback()
        raise
