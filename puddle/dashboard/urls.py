from django.urls import path

from . import views

app_name="dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('sales_orders/', views.sales_orders, name='sales_orders'),
    path('purchase_orders/', views.purchase_orders, name='purchase_orders'),
]
