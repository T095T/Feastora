from django.shortcuts import get_object_or_404, render
from django.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *

# Create your views here.

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, user):
        cart , _ = Cart.objects.get_or_create(customer = user.customer_profile)
        return cart
     
    @action(detail=True,methods=['post'])    
    def add(self,request):
        user = request.user
        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity')
        
        menu_item = get_object_or_404(MenuItem,id=menu_item_id)
        cart = self.get_cart(user)
        
        if cart.restaurant and cart.restaurant != menu_item.category.restaurant:
            return Response({'error': 'Cannot add item from different restaurant'}, status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item,created = Cart.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults=(
                'quantity':quantity,
                'price_at_add_time':menu_item.price,)
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return Response({"message:" "Item added in cart successfully"},status=status.HTTP_201_CREATED)
        
            