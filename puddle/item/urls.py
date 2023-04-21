from django.urls import path

from . import views
from .views import(
    OrderSummaryView
)

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<int:pk>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
]
