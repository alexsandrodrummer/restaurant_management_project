from django.urls import path
from .views import MenuItemsByCategoryView, MenuItemUpdateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"items", MenuItemUpdateViewSet, basename='menu-item')
router.register(r"items", MenuItemsByCategoryView, basename='menu-item')

urlpatterns =  router.urls
    