from decimal import Decimal
from store.models import Product
from cart.forms import CartAddProductForm


def cart(request):
    cart = request.session.get("cart")
    total_price = 0
    total_items = 0
    if cart:
        products = Product.objects.filter(id__in=cart.keys())
        for product in products:
            str_product_id = str(product.id)
            cart[str_product_id]["product"] = product
            cart[str_product_id]["price"] = Decimal(cart[str_product_id]["price"])
            cart[str_product_id]["total_price"] = (
                cart[str_product_id]["price"] * cart[str_product_id]["quantity"]
            )
            cart[str_product_id]["update_quantity_form"] = CartAddProductForm(
                initial={"quantity": cart[str_product_id]["quantity"], "override": True}
            )
            total_price += cart[str_product_id]["total_price"]
            total_items += cart[str_product_id]["quantity"]
    else:
        cart = {}

    return {"cart": cart, "total_price": total_price, "total_items": total_items}
