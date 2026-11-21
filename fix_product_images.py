
from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()

image_mapping = {
    "Cheese Burger": "cheese_burger.jpg",
    "Margherita Pizza": "margherita_pizza.jpg",
    "French Fries": "french_fries.jpg",
    "Veg Sandwich": "veg_sandwich.jpg",
    "Cold Coffee": "cold_coffee.jpg",
    "White Sauce Pasta": "white_sauce_pasta.jpg",
    "Paneer Pizza": "paneer_pizza.jpg",
    "Chocolate Shake": "chocolate_shake.jpg"
}

with app.app_context():

    for product_name, image_filename in image_mapping.items():

        product = Product.query.filter_by(
            name=product_name
        ).first()

        if product:
            product.image_filename = image_filename
            print(f"Updated: {product.name} -> {image_filename}")
        else:
            print(f"Product not found: {product_name}")

    db.session.commit()

    print("\nAll available product images assigned successfully!")
