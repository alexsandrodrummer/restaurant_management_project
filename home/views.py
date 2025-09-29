from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import MenuCategory
from .serializers import MenuItemSerializer


class MenuItemsByCategoryView(ListAPIView):
    serializer_class = MenuItemSerializer
    def get_queryset(self):
        qs = MenuItem.objects.filter(is_active=True).select_related('category')
        category_id = self.request.query_params.get('category_id')
        category_name = self.request.query_params.get('category')
        if category_id:
            return qs.filter(category_id=category_id)
        if category_name:
            return qs.filter(category__name__iexact=category_name)
        return qs.none()
    