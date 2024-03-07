from django.urls import path
from apps.products.views import ListProducts, DetailDeleteProduct, EditProduct, CreateProduct, ListProductsByCategory

urlpatterns = [
    path('list', ListProducts.as_view(), name='product_list'),
    path('list/<int:category_id>', ListProductsByCategory.as_view(),
         name='product_list_by_category'),
    path('create', CreateProduct.as_view(), name='product_create'),
    path('detail/<str:slug>', DetailDeleteProduct.as_view(),
         name='product_delete_detail'),
    path('edit/<str:slug>', EditProduct.as_view(), name='product_detail'),
]
