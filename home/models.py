from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    name = models.charField(max_length=100, inique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Menu category"
        verbose_name_plural = "Menu categories"

    def __str__(self):
        return self.name