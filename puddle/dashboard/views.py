from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Prefetch
from datetime import datetime, timedelta
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce, Cast

# Create your views here.
from item.models import Item, Order, OrderItem

@login_required
def index(request):
    today = datetime.now().date()
    ten_days_ago = today - timedelta(days=9)  # Lấy 10 ngày gần nhất

    income_list = OrderItem.objects.filter(
        ordered=True,
        order__ordered_date__date__range=[ten_days_ago, today],
        user=request.user  # Lọc theo người dùng hiện tại
    ).values('order__ordered_date__date').annotate(
        total_income=Coalesce(
            Sum(F('quantity') * F('item__price'), output_field=FloatField()),
            0.0
        )
    ).order_by('order__ordered_date__date')

    date_income_list = []
    for income in income_list:
        date = income['order__ordered_date__date']
        total_income = income['total_income']
        date_income_list.append({'date': date, 'total_income': total_income})

    # Xác định các ngày không có dữ liệu và đặt giá trị thu nhập là 0
    date_range = [ten_days_ago + timedelta(days=i) for i in range(10)]
    for date in date_range:
        if date not in [income['date'] for income in date_income_list]:
            date_income_list.append({'date': date, 'total_income': 0.0})

    # Sắp xếp theo ngày
    date_income_list.sort(key=lambda x: x['date'])

    for date in date_income_list:
        print(date)
    #danh sách sản phẩm bán được
    items = Item.objects.filter(created_by=request.user).annotate(quantity_sold=models.Sum(models.Case(models.When(orderitem__ordered=True, then=models.F('orderitem__quantity')), default=0, output_field=models.IntegerField()))).order_by('-quantity_sold')[:6]
    item_quantity_list = [(item, item.quantity_sold) for item in items]
    context = {
        'date_income_list': date_income_list,
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
