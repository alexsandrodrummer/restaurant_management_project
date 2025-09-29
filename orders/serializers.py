from rest_framework import serializers
from .models import Order

class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItemSerializer
        fields = ["id", "product_name", "unit_price", "quantity", "line_total"]

    def get_line_total(self, obj):
        return obj.unit_price * obj.quantity



class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True,read_only=True)
    status = serializers.charField(source="status.name", default=None, read_only=True)
    date = serializers.DateTimeField(source="created_at", format="%y-%m-%d %H:%M:%S")
    class Meta:
        model = Order
        fields = ["id", "code", "total", "created_at"]
        read_only_fields = ["id", "created_at"]