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


class StandardREsultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class MenuItemSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 
    GET /api/menu/items/search/?q=burger&page=1&page_size=10
    Busca case-Insensitive por nome (name__icontains).

    """


    def get_queryset(self):
        q = (self.request.query_params.get("q")or "").strip()
        base_qs = MenuItem.objects.select_related("category").filter(is_active=True)
        if not q:
            return base_qs.none()
        return base_qs.filter(Q(name__icontains))

    def list(self, request, *args, **kwargs):
        q= (request.query_params.get("q") or "").strip()
        if not q:
            return Response({"detail": "provide query paramenter 'q'."}, status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)


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