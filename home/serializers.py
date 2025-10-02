from rest-framework import serializers
from .models import MenuItem 


class MenuCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name',read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'category', 'category_id', 'is_active']
        read_only_fields = ['category']


class MenuItemUpdateSerializer (serializer.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "is_active", "category"]
        extra_kwargs = {
            "name":{"required": False},
            "description": {"required": False, "allow_blank": True},
            "price": {"required":False},
            "is_active":{"required": False },
            "category": {"required": False},
        }
    def validate_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("price must be a positive number.")
        
        return value
