from decimal import Decimal

from app import create_app
from app.extensions import db
from app.models import Product

app = create_app()

sample_products = [
    {
        "name": "Cheese Burger",
        "description": "Burger with cheese and fresh vegetables.",
        "category": "Burger",
        "price": Decimal("149.00"),
        "stock": 20
    },
    {
        "name": "Margherita Pizza",
        "description": "Classic pizza with mozzarella cheese.",
        "category": "Pizza",
        "price": Decimal("249.00"),
        "stock": 15
    },
    {
        "name": "French Fries",
        "description": "Crispy golden potato fries.",
        "category": "Snacks",
        "price": Decimal("99.00"),
        "stock": 30
    },
    {
        "name": "Veg Sandwich",
        "description": "Fresh vegetable sandwich.",
        "category": "Sandwich",
        "price": Decimal("119.00"),
        "stock": 20
    },
    {
        "name": "Cold Coffee",
        "description": "Chilled creamy cold coffee.",
        "category": "Drinks",
        "price": Decimal("89.00"),
        "stock": 25
    },
    {
        "name": "White Sauce Pasta",
        "description": "Creamy white sauce pasta.",
        "category": "Pasta",
        "price": Decimal("179.00"),
        "stock": 15
    },
    {
        "name": "Paneer Pizza",
        "description": "Pizza topped with paneer.",
        "category": "Pizza",
        "price": Decimal("299.00"),
        "stock": 12
    },
    {
        "name": "Chocolate Shake",
        "description": "Rich chocolate milkshake.",
        "category": "Drinks",
        "price": Decimal("129.00"),
        "stock": 20
    }
]

with app.app_context():
    added = 0

    for item in sample_products:
        existing = Product.query.filter_by(
            name=item["name"]
        ).first()

        if not existing:
            db.session.add(Product(**item))
            added += 1

    db.session.commit()

    print(f"Successfully added {added} food products!")
    print(f"Total products: {Product.query.count()}")