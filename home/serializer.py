from rest-framework import serializers
from .models import MenuItem 


class MenuCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name',read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'category', 'category_id', 'is_active']
        read_only_fields = ['category']