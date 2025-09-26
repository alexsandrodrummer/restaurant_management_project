from django.contrib import admin
from .models import Order, OrderStatus

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'total','created_at']

@admin.register(Order)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)