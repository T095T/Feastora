from django.db import models
from accounts.models import CustomerProfile, RestaurantProfile,RiderProfile
from menu.models import MenuItem
# Create your models here.

class Order(models.Model):
    class Status(models.TextChoices):
        PLACED  = 'PLACED', 'Placed'
        ACCEPTED   = 'ACCEPTED',   'Accepted'
        PREPARING  = 'PREPARING',  'Preparing'
        PICKED     = 'PICKED',     'Picked Up'
        DELIVERED  = 'DELIVERED',  'Delivered'
        CANCELLED  = 'CANCELLED',  'Cancelled'

    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='orders')
    restaurant = models.ForeignKey(RestaurantProfile,on_delete=models.CASCADE,related_name='orders')
    rider = models.ForeignKey(RiderProfile,on_delete=models.SET_NULL,related_name='orders',null=True,blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PLACED)

    delivery_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    picked_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.customer.user.email} - {self.status}"


    
class OrderItem(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item       = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name='order_items')
    quantity        = models.PositiveIntegerField(default=1)
    item_name       = models.CharField(max_length=100)
    price_at_order  = models.DecimalField(max_digits=10,decimal_places=2)
    
    
    class Meta:
        ordering = ['item_name']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.item_name} — ₹{self.total_price}"

    @property
    def total_price(self):
        return self.price_at_order * self.quantity
