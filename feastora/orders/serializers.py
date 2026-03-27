from rest_framework import serializers
from .models import *
from menu.models import MenuItem
from accounts.models import CustomerProfile, RestaurantProfile, RiderProfile

class OrderCreateSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=RestaurantProfile.objects.all())
    rider = serializers.PrimaryKeyRelatedField(queryset=RiderProfile.objects.all(), required=False, allow_null=True)
    delivery_address = serializers.CharField(max_length=255)
    items = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all()))
    status = serializers.ChoiceField(choices=Order.Status.choices, default=Order.Status.PLACED)

    def validate_items(self,value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def validate_delivery_address(self,value):
        if not value:
            raise serializers.ValidationError("Delivery address is required.")
        return value

    def create(self, validated_data):
        customer = validated_data.pop('customer')
        restaurant = validated_data.pop('restaurant')
        rider = validated_data.pop('rider', None)
        delivery_address = validated_data.pop('delivery_address')
        items = validated_data.pop('items')
        status = validated_data.pop('status', Order.Status.PLACED)

        order = Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            rider=rider,
            delivery_address=delivery_address,
            status=status,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                menu_item=item,
                item_name=item.name,
                price_at_order=item.price,
            )
        return order
    

class OrderUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices, required=True)

    def validate_status(self,value):
        if value not in [Order.Status.ACCEPTED, Order.Status.PREPARING, Order.Status.PICKED, Order.Status.DELIVERED, Order.Status.CANCELLED]:
            raise serializers.ValidationError("Invalid status.")
        return value
    
    def update(self,instance,validated_data):
        instance.status = validated_data.get('status',instance.status)
        instance.save()
        return instance
    
class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','customer','restaurant','rider','delivery_address','status','created_at','updated_at','accepted_at','picked_at','cancelled_at','delivered_at']