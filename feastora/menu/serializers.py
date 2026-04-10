from rest_framework import serializers
from .models import *
from restaurant.models import Restaurant


class MenuCategoryCreateSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)
    images = serializers.ImageField(allow_empty_file=True,required=False)
    order = serializers.IntegerField(default=0)

    def validate_order(self,value):
        if value < 0:
            raise serializers.ValidationError("Order must be greater than or equal to 0.")
        return value 

    def create(self,validated_data):
        return MenuCategory.objects.create(**validated_data)

class MenuCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id','name','description','images','order']

    
class MenuCategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,required=True)
    description = serializers.CharField(allow_blank=True,required=False)
    images = serializers.ImageField(allow_empty_file=True,required=False)
    order = serializers.IntegerField(default=0)

    def validate_order(self,value):
        if value < 0:
            raise serializers.ValidationError("Order must be greater than or equal to 0.")
        return value 

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.images = validated_data.get('images',instance.images)
        instance.order = validated_data.get('order',instance.order)
        instance.save()
        return instance

    class Meta:
        model = MenuCategory
        fields = ['name','description','images']


class MenuCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['name','description','images']


class MenuItemCreateSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())
    name = serializers.CharField(max_length=100,required=True)
    description = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=10,decimal_places=2,required=True)
    images = serializers.ImageField(allow_empty_file=True,required=False)
    food_type = serializers.ChoiceField(choices=MenuItem.FoodType.choices,required=True)
    isAvailable = serializers.BooleanField(default=True)

    def validate_name(self,value):
        if not value :
            raise serializers.ValidationError("Name cannot be numeric.")
        elif value.isnumeric():
            raise serializers.ValidationError("Name cannot be numeric.")
        else:
            return value
        

    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError("Price cannot be zero or negative")
        return value

    def create(self,validated_data):
        return MenuItem.objects.create(**validated_data)


class MenuItemUpdateSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MenuCategory.objects.all())
    name = serializers.CharField(max_length=100,required=True)
    description = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=10,decimal_places=2,required=True)
    images = serializers.ImageField(allow_empty_file=True,required=False)
    food_type = serializers.ChoiceField(choices=MenuItem.FoodType.choices,required=True)
    isAvailable = serializers.BooleanField(default=True)

    def validate_name(self,value):
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_price(self,value):
        if value <0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.price = validated_data.get('price',instance.price)
        instance.images = validated_data.get('images',instance.images)
        instance.food_type = validated_data.get('food_type',instance.food_type)
        instance.category = validated_data.get('category',instance.category)
        instance.isAvailable = validated_data.get('isAvailable',instance.isAvailable)
        instance.save()
        return instance

class MenuItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','name','description','price','images','food_type','isAvailable']
