from django.urls import path
from apps.category.views import ListCreateCategory, DetailDeleteCategory, ListAllCategories

urlpatterns = [
    path('', ListCreateCategory.as_view(), name='list_categories'),
    path('all', ListAllCategories.as_view(), name='list_all_categories'),
    path('<str:slug>', DetailDeleteCategory.as_view(), name='detail_categories'),
]
