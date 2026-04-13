from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from accounts.models import CustomerProfile
from restaurant.models import Restaurant
from menu.models import MenuItem

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "ACTIVE"),
        ("CHECKED_OUT", "CHECKED_OUT"),
    )

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name="carts")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(status="ACTIVE"),
                name="unique_active_cart_per_user"
            )
        ]

    def __str__(self):
        return f"Cart {self.id} - {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_add_time = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'menu_item']

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"