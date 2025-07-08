from django.urls import path
from .views import *

urlpatterns = [
    path('basket/', BasketList.as_view(), name='basket_list'),
    path('search', SearchList.as_view(), name='search_list'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('delete/<int:pk>', DeleteProductView.as_view(), name='delete_product'),
    path('<slug:animal_sort>/', CategoryListView.as_view(), name='category_list'),
    path('<slug:animal_sort>/<slug:subcategory>',  ProductListView.as_view(), name='product_list'),
    path('<slug:animal_sort>/<slug:subcategory>/<slug:product>', ProductDetailView.as_view(), name='product_description'),
]
