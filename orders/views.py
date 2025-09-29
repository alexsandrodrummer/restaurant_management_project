# orders/views.py
from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ["code"]                    # nada de customer__name aqui
    ordering_fields = ["created_at", "total"]   # apenas campos válidos
    ordering = ["-created_at"]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderHistoryview(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, django_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ["code"]
    ordering_fields = ["created_at", "total"]
    ordering = ["-created_at"]


    def get_queryset(self):

        return(
            Order.objects
            .filter(user=self.request.user)
            .select_related("status", "user")
            .prefetch_related("items")
            .order_by("-created_at")
        )
    # opcional: você pode omitir se já definiu no settings
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = OrderFilter
#     search_fields = ["customer__name", "code"]   # pesquisa textual
#     ordering_fields = ["created_at", "total"]    # ordenação via ?ordering=-total

