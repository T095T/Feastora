import django_filters
from .models import *

class RestaurantFilters(django_filters.FilterSet):
    class Meta:
        model=Restaurant
        fields=['name','address','cuisine','speciality']
        

