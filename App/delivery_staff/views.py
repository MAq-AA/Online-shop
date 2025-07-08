from django.shortcuts import render
from django.views.generic import *
from .models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
