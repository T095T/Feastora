from rest_framework import serializers

from menu.serializers import MenuCategoryListSerializer, MenuItemListSerializer
from accounts.models import User
from restaurant.models import Restaurant


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','address','phoneNumber','email','description','banner','logo']

    
class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name','address','phoneNumber','email','description','banner','logo','isActive','isVerified','reviews','rating','cuisine','isOpen','speciality']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        categories = data['categories'] = MenuCategoryListSerializer(instance.categories.all(), many=True).data
        for category in categories:
            category['menu_items'] = MenuItemListSerializer(category['items'].all(), many=True).data
        data['categories'] = categories
        return data
    
class RestaurantCreateSerializer(serializers.Serializer):
    email            = serializers.EmailField()
    phoneNumber      = serializers.CharField(max_length=15)    # login + restaurant contact phone
    password         = serializers.CharField(write_only=True, min_length=8)
    restaurant_name  = serializers.CharField(max_length=200)
    address          = serializers.CharField()
    cuisine          = serializers.CharField(max_length=100, required=False, allow_blank=True)
    speciality       = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        if User.objects.filter(phoneNumber=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        restaurant_name  = validated_data.pop('restaurant_name')
        address          = validated_data.pop('address')
        cuisine          = validated_data.pop('cuisine', '')
        speciality       = validated_data.pop('speciality', '')
        phoneNumber      = validated_data['phoneNumber']
        email             = validated_data['email']

        user = User.objects.create_user(
            email    = email,
            phoneNumber = phoneNumber,
            password = validated_data['password'],
            role     = User.Role.RESTAURANT
        )
        Restaurant.objects.create(
            user    = user,
            name    = restaurant_name,
            phoneNumber = phoneNumber,
            address = address,
            email = email,
            cuisine = cuisine,
            speciality = speciality
        )
        return user

    