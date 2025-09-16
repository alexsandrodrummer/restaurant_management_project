# products/views.py
from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item
from .serializers import ItemSerializer
from .filters import ItemFilter
# (opcional) para forçar paginação específica:
# from restaurant_management.pagination import DefaultPagination

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by("-created_at")
    serializer_class = ItemSerializer

    # pagination_class = DefaultPagination  # normalmente não precisa (usa a global)

    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = ItemFilter
    search_fields = ["item_name"]                 # GET ?search=camisa
    ordering_fields = ["created_at", "item_price", "item_name"]  # GET ?ordering=-item_price
    ordering = ["-created_at"]                    # ordenação padrão

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
