from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Prefetch

# Create your views here.
from item.models import Item, Order, OrderItem

@login_required
def index(request):
    # items = Item.objects.filter(created_by=request.user)
    # order_items = OrderItem.objects.filter(item__created_by=request.user)

    # return render(request, 'dashboard/index.html', {
    #     'items':items,
    #     'order_items': order_items,
    # })
    items = Item.objects.filter(created_by=request.user).annotate(quantity_sold=models.Sum(models.Case(models.When(orderitem__ordered=True, then=models.F('orderitem__quantity')), default=0, output_field=models.IntegerField()))).order_by('-quantity_sold')[:6]
    item_quantity_list = [(item, item.quantity_sold) for item in items]
    context = {
        'item_quantity_list': item_quantity_list
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def purchase_orders(request):
    purchase_orders = Order.objects.filter(user = request.user, ordered = True).order_by('-id')
    context = {
        'purchase_orders' :purchase_orders,
    }
    return render(request, 'dashboard/purchase_orders.html', context)

# @login_required
# def sales_orders(request):
#     sales_items = OrderItem.objects.filter(user=request.user, ordered=True)
#     context = {
#         'sales_items':sales_items,
#     }
#     return render(request, 'dashboard/sales_orders.html', context)

@login_required 
def sales_orders(request):
    sales_orders = OrderItem.objects.filter(ordered=True, item__created_by=request.user).order_by('-id')
    context = {
        'sales_orders':sales_orders,
    }
    return render(request, 'dashboard/sales_orders.html', context) 
