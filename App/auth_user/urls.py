from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change/<int:pk>', ChangeView.as_view(), name='change'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete'),
]