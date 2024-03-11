from django.urls import path
from apps.category.views import ListCreateCategory, DetailDeleteUpdateCategory, ListAllCategories

urlpatterns = [
    path('', ListCreateCategory.as_view(), name='list_categories'),
    path('all', ListAllCategories.as_view(), name='list_all_categories'),
    path('<str:slug>', DetailDeleteUpdateCategory.as_view(),
         name='detail_categories'),
]
