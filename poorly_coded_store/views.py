from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

#def checkout(request):
#    quantity_from_form = int(request.POST["quantity"])
#    price_from_form = float(request.POST["price"])
#    total_charge = quantity_from_form * price_from_form
#    print("Charging credit card...")
#    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

#    context = {
#        "current_charge" : total_charge,
#        "orders": Order.objects.all()
#    }
#    return redirect('/thankyou',"current_charge")

#def thankyou(request,current_charge):
#    all_charges = orders.objects.all().aggregate(Sum("total_price"))['total_price__sum'] or 0.00
#    all_charges=float(all_charges)#
#
#    all_items = Order.objects.all().aggregate(Sum("quantity_ordered"))['quantity_ordered__sum'] or 0
#
#    context = {
#        "current_charge" : current_charge,
#        "all_charge" : all_charges,
#        "total_items" : all_items
#    }
    #return redirect('/thankyou',context)
#    return render(request, "store/thankyou.html", context)

def purchase(request):
    if request.method == 'POST':
        this_product = Product.objects.filter(id=request.POST["id"])
        if not this_product:
            return redirect('/')
        else:
            quantity_from_form = int(request.POST["quantity"])
            #price_from_form = float(request.POST["price"])
            price_from_form = float(this_product[0].price)
            total_charge = quantity_from_form * price_from_form
            print("Charging credit card...")
            Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
            return redirect('/checkout')
    else:
        return redirect('/')

def checkout(request):
    last = Order.objects.last()
    current_charge=last.total_price

    all_charges = Order.objects.all().aggregate(Sum("total_price"))['total_price__sum'] or 0.00
    all_charges=float(all_charges)

    all_items = Order.objects.all().aggregate(Sum("quantity_ordered"))['quantity_ordered__sum'] or 0

    context = {
        "current_charge" : current_charge,
        "all_charge" : all_charges,
        "total_items" : all_items

    }

    return render(request, "store/checkout.html",context)