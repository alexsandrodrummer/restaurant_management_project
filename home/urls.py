from django.urls import path
from .views import MenuItemsByCategoryView

urlpatterns = [
    path('menu/items/by-category/', MenuItemsByCategoryView.as.view(), name='menu-items-by-category'),
    
]