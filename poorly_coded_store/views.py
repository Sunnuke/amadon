from django.shortcuts import render, redirect
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    if 'orders' not in request.session:
        request.session['orders'] = int(request.POST["quantity"])
    if 'total' not in request.session:
        request.session['total'] = Product.objects.get(id=int(request.POST["price"])).price
    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(Product.objects.get(id=int(request.POST["price"])).price)
    total_charge = quantity_from_form * price_from_form
    print("Charging credit card...", total_charge)
    request.session['orders'] += quantity_from_form
    request.session['total'] += total_charge
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    return redirect('checkout/processed')

def process(request):
    context = {
        'item': Order.objects.last(),
        'orders': request.session['orders'],
        'total': request.session['total']
    }
    return render(request, "store/checkout.html", context)
