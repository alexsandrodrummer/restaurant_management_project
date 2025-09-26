from django.db import models

class Order(models.Model):
    code = models.CharField(max_length=50, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.code

class OrderStatus (models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Order status"
        verbose_name_plural = "Order statuses"
        ordering = ("name",)

    def __str__(self):
        return self.name