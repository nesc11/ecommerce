from decimal import Decimal


def cart(request):
    cart = request.session.get("cart", {})
    total_items = 0
    total_price = 0
    for key, item in cart.items():
        total_price += item["quantity"] * Decimal(item["price"])
        total_items += item["quantity"]

    return {"total_items": total_items, "total_price": total_price}
