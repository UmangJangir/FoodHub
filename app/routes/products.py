
from flask import Blueprint, render_template, abort
from app.models import Product

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


@products_bp.route("/")
def products_list():

    products = Product.query.filter_by(
        is_available=True
    ).all()

    return render_template(
        "products.html",
        products=products
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    if not product.is_available:
        abort(404)

    return render_template(
        "product_detail.html",
        product=product
    )
