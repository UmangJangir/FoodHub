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
    updated = 0

    for name, filename in image_mapping.items():
        product = Product.query.filter_by(name=name).first()

        if product:
            product.image_filename = filename
            updated += 1

    db.session.commit()

    print(f"Successfully updated {updated} product images!")
