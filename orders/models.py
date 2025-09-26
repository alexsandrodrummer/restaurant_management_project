from django.db import models

class OrderStatus(models.Model):
    name = models.charField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Order status"
        verbose_name_plural = "Order statuses"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Order(models.Model):
    code = models.charField(max_length=50, unique=True, db_index=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    status = models.Foreignkey(
        OrderStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.code