from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = "core"
urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/index.html'), name='logout'),
    path('settings/', views.settings, name='settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile/<str:pk>/', views.profile, name='profile')
]
