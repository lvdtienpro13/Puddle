from django.urls import path
from . import views

app_name = 'rating'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:order_item_id>/', views.rating, name='rating'),
]
