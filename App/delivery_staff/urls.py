from django.urls import path
from .views import *

urlpatterns = [
    path('list_of_order/', OrderListView.as_view(), name='order_list1'),
]
