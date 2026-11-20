
from datetime import datetime, timezone

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    delivery_person_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    total_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    payment_method = db.Column(
        db.String(30),
        nullable=False,
        default="COD"
    )

    payment_status = db.Column(
        db.String(30),
        nullable=False,
        default="pending"
    )

    order_status = db.Column(
        db.String(30),
        nullable=False,
        default="placed"
    )

    delivery_address = db.Column(
        db.Text,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan",
        lazy=True
    )

    customer = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref="customer_orders"
    )

    delivery_person = db.relationship(
        "User",
        foreign_keys=[delivery_person_id],
        backref="delivery_orders"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=True
    )

    product_name = db.Column(
        db.String(120),
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    product = db.relationship("Product", lazy=True)
