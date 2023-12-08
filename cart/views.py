from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from store.models import Product
from .forms import CartAddProductForm


# Create your views here.
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    str_product_id = str(product_id)
    cart = request.session.get("cart", {})
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if str_product_id not in cart:
            cart[str_product_id] = {"quantity": 0, "price": str(product.price)}
        if cd["override"]:
            cart[str_product_id]["quantity"] = cd["quantity"]
        else:
            cart[str_product_id]["quantity"] += cd["quantity"]
        request.session["cart"] = cart
    return redirect("cart:cart-detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del request.session["cart"][str(product_id)]
        request.session.modified = True
    return redirect("cart:cart-detail")


def cart_detail(request):
    return render(request, "cart/cart_detail.html")
