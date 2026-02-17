from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.username 


from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"




class Product(models.Model):
    name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField()

    min_threshold = models.PositiveIntegerField()

    expiration_date = models.DateField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_low_stock(self):
        return self.quantity <= self.min_threshold

    def has_expiry(self):
        if self.expiration_date:
            return self.expiration_date <= timezone.now().date()
        return False

    def __str__(self):
        return f"{self.name} - {self.category.name}"
