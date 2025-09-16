# products/filters.py
from django_filters import rest_framework as filters
from .models import Item

class ItemFilter(filters.FilterSet):
    # Preço mínimo/máximo: ?min_price=10&max_price=50
    min_price = filters.NumberFilter(field_name="item_price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="item_price", lookup_expr="lte")

    # Intervalo de datas de criação:
    # ?created_after=2025-09-01&created_before=2025-09-16
    created = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Item
        fields = {
            "item_price": ["exact"],   # ?item_price=19.90
            # você pode expor outros campos exatos aqui se quiser
        }
