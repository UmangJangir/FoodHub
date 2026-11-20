from app.extensions import db
from app.models import Cart, CartItem, Product


def get_or_create_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    return cart


def add_to_cart(user_id, product_id, quantity=1):

    product = db.session.get(Product, product_id)

    if not product or not product.is_available:
        return False, "Product is not available."

    if quantity < 1:
        return False, "Invalid quantity."

    cart = get_or_create_cart(user_id)

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    current_quantity = cart_item.quantity if cart_item else 0
    new_quantity = current_quantity + quantity

    if new_quantity > product.stock:
        return False, "Not enough stock available."

    if cart_item:
        cart_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return True, "Product added to cart successfully!"


def update_cart_item(user_id, item_id, quantity):

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return False, "Cart not found."

    item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()

    if not item:
        return False, "Cart item not found."

    if quantity < 1:
        return False, "Quantity must be at least 1."

    if not item.product or quantity > item.product.stock:
        return False, "Requested quantity is not available."

    item.quantity = quantity
    db.session.commit()

    return True, "Cart quantity updated successfully!"


def remove_cart_item(user_id, item_id):

    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return False, "Cart not found."

    item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()

    if not item:
        return False, "Cart item not found."

    db.session.delete(item)
    db.session.commit()

    return True, "Product removed from cart!"
