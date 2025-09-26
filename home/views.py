from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import MenuCategory
from .serializers import MenuCategorySerializer


class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all().order_by('name')
    serializer_class = MenuCategorySerializer
    permission_classes = []
    authentication_classes = []