# orders/filters.py
from django_filters import rest_framework as filters
from .models import Order

class OrderFilter(filters.FilterSet):
    # Faixa de total ?min_total=10&max_total=100
    min_total = filters.NumberFilter(field_name="total", lookup_expr="gte")
    max_total = filters.NumberFilter(field_name="total", lookup_expr="lte")

    # Intervalo de datas ?created_after=YYYY-MM-DD&created_before=YYYY-MM-DD
    created = filters.DateFromToRangeFilter(field_name="created_at")

    # Busca por código exato/contains também pode ser exposta via fields (ou via SearchFilter)
    code_icontains = filters.CharFilter(field_name="code", lookup_expr="icontains")

    class Meta:
        model = Order
        # Liste apenas campos que EXISTEM no modelo
        fields = {
            "code": ["exact", "icontains"],
            "total": ["exact", "gte", "lte"],
            "created_at": ["exact"],  # você pode omitir se usar o 'created' acima
        }
