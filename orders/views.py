from decimal import Decimal
from django.shortcuts import render, HttpResponse
from store.models import Product
from .models import OrderItem
from .forms import OrderForm


def order_create(request):
    cart = request.session.get("cart")
    if not cart:
        return HttpResponse("You cant place and order without items")
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for key, item in cart.items():
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=int(key)),
                    price=Decimal(item["price"]),
                    quantity=item["quantity"],
                )
            del request.session["cart"]
        return render(request, "orders/order_created.html")
    return render(request, "orders/order_create.html", {"form": form})
