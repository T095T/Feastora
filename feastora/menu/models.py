from django.db import models
from accounts.models import RestaurantProfile



class MenuCategory(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile,on_delete=models.CASCADE,related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    images = models.ImageField(upload_to='menu_categories/',blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order','name']
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    class FoodType(models.TextChoices):
        VEG      = 'veg',      'Vegetarian'
        NON_VEG  = 'non_veg',  'Non-Vegetarian'
        VEGAN    = 'vegan',    'Vegan'


    category = models.ForeignKey(MenuCategory,on_delete=models.CASCADE,related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    images = models.ImageField(upload_to='menu_items/',blank=True)
    food_type = models.CharField(max_length=10,choices=FoodType.choices)
    isAvailable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price}"