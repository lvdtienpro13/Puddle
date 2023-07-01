from django.urls import path
from . import views

app_name = 'searchbyimage'

urlpatterns = [
    path('', views.search_item, name='search_item'),
]
