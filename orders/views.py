# orders/views.py
from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter
from rest_framework.views import APIView
from .models import Coupon


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

class CouponValidationView(APIView):
    permission_classes = [AllowAny] #Ajuste se quiser restringir 

    
    def post(self, request):
        code = (request.data.get("code") or"").strip()
        if not code:
            return Response({"detail": "Informe o campo 'code'."}, status=status.HTTP_400_BAD_REQUEST)
        

        today = timezone.now().date()

        coupon = (
            Coupon.objects
            .filter(code__iexact=code, is_active=True,
            valid_from_lte=today, valid_until__gte=today)
            .first()
        )

        if not coupon:
            return Response({"detail": "Cupom inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "success": True,
            "code": coupon.code,
            "discount_percentage": str(coupon.discount_percentage), # ex.: "0.10"
            "valid_from": coupon.valid_from.isoformat(),
            "valid_until": coupon.valid_until.isoformat(),
        }, status=status.HTTP_200_OK) 