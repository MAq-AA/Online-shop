from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsListView.as_view(), name='News_list'),
    path('post/<int:pk>/', NewsDetailView.as_view(), name='News_detail'),
    path('post/new/', NewsCreateView.as_view(), name='News_create'),
    path('post/<int:pk>/edit/', NewsUpdateView.as_view(), name='News_edit'),
    path('post/<int:pk>/delete/', NewsDeleteView.as_view(), name='News_delete'),
]
