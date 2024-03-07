from django.urls import path
from apps.carts.views import ListCreateCartView, DetailCartView
urlpatterns = [
    path('', ListCreateCartView.as_view(), name='carts'),
    path('<int:pk>', DetailCartView.as_view(), name='cart_detail'),
]
