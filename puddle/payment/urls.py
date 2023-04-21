from django.urls import path
from . import views

app_name='payment'

urlpatterns = [
    path('checkout/<int:pk>/',views.checkout, name='checkout'),
    path('process/<int:pk>/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
