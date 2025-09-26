from django.urls import path
from .views import MenuCategoryListView

urlpatterns = [
    path('menu/categories/', MenuCategoryListView.as.view(), name='meni-category-list'),
    
]