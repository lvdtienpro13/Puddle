from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    path('', views.inbox1, name='inbox1'),
    path('<int:pk>/', views.inbox, name='inbox'),
    # path('<int:pk>/', views.detail, name='detail')
]
