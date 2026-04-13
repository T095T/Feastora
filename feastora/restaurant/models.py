from django.conf import settings
from django.db import models

from accounts.models import User


class Restaurant(models.Model):
    # Used throughout the codebase as `request.user.restaurant_profile`
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="restaurant_profile",
    )

    # Base restaurant fields (used by restaurant/serializers.py and restaurant/views.py)
    name = models.CharField(max_length=200)
    address = models.TextField()
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="restaurant/logo/", blank=True, null=True)
    banner = models.ImageField(upload_to="restaurant/banner/", blank=True, null=True)

    isActive = models.BooleanField(default=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    reviews = models.TextField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    
    cuisine = models.CharField(max_length=100, blank=True)
    isOpen = models.BooleanField(default=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    speciality = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name}"