import django_filters
from .models import *


class MenuFilter(django_filters.FilterSet):
    class Meta:
        model = Menu
        fields = ['restaurant']

class MenuCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = MenuCategory
        fields = ['menu','isAvailable']

class MenuItemFilter(django_filters.FilterSet):
    class Meta:
        model = MenuItem
        fields = ['category','food_type','isAvailable']