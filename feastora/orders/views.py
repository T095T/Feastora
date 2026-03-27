
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderUpdateSerializer,
    
)
from accounts.models import RiderProfile
# from accounts.permissions import IsCustomer, IsRestaurant, IsRider

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]


    def get_query_set(self):
        user = self.request.user

        if user.is_authenticated and user.is_customer:
            return Order.objects.filter(customer=user.customer_profile).select_related('restaurant','rider').prefetch_related('items')

        if user.is_authenticated and user.is_rider:
            return Order.objects.filter(rider=user.rider_profile).select_related('restaurant','customer').prefetch_related('items')

        if user.is_authenticated and user.is_restaurant:
            return Order.objects.filter(restaurant=user.restaurant_profile).select_related('customer','rider').prefetch_related('items')
        
    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update':
            return OrderUpdateSerializer
        return OrderListSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = OrderCreateSerializer(data  = request.data , context = {'request':request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderListSerializer(order).data,status=status.HTTP_201_CREATED)