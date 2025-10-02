from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import MenuCategory
from .serializers import MenuItemSerializer
import logging
from django.db import transaction 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permission import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin


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
    

logger = logging.getLogger(__name__)

class MenuItemUpdateViewSet(UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    PUT /api/menu/items/{id}/
    PATCH /api/menu/items/{id}/
    """

    queryset = MenuItem.objects.select_related("category").all()
    serializer_class = MenuItemUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as exc:
            logger.exception("Erros updating MenuItem> %s", exc)
            return Response({"detail": "unable to update menu item."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except Exception as exc:
            logger.exception("Error partially updatinf MenuItem: %s", exc)
            return Response({"detail": "unable to update manu item ."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)