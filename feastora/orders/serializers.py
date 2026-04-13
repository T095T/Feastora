from decimal import Decimal
from rest_framework import serializers
from .models import *
from menu.models import MenuItem
from restaurant.models import Restaurant
from django.db import transaction

class OrderCreateSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    delivery_address = serializers.CharField(max_length=255)
    items = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all()))

    #to check if the items belong to the selected restaurant
    def validate(self, data):
        restaurant = data.get('restaurant')
        items = data.get('items', [])

        if not items:
            raise serializers.ValidationError({"items": "At least one item is required."})

        for item in items:
            if item.category.menu.restaurant_id != restaurant.id:
                raise serializers.ValidationError(
                    {"items": "Can only select items from one restaurant"}
                )
            if not item.isAvailable:
                raise serializers.ValidationError(f"{item.name} is not available.")
        return data


    def validate_delivery_address(self,value):
        if not value.strip():
            raise serializers.ValidationError("Delivery address is required.")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if not hasattr(user, 'customer_profile'):
            raise serializers.ValidationError("Customer profile not found.")

        customer = user.customer_profile
        restaurant = validated_data.pop('restaurant')
        delivery_address = validated_data.pop('delivery_address')
        items_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                restaurant=restaurant,
                delivery_address=delivery_address,
                status=Order.Status.PLACED,
                delivery_fee=Decimal("0.00"),
            )
            for item in items_data:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    item_name=item.name,
                    price_at_order=item.price,
                    quantity=1,
                )
            order.calculate_total()
            order.save()
        return order
    

class OrderUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices, required=True)
    
    def update(self,instance,validated_data):
        instance.status = validated_data.get('status',instance.status)
        instance.save()
        return instance
    
class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id", "customer", "restaurant", "rider",
            "delivery_address", "status",
            "subtotal", "delivery_fee", "total",
            "created_at", "updated_at",
            "accepted_at", "picked_at", "cancelled_at", "delivered_at",
        ]