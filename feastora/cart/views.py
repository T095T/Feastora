from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status, viewsets
from menu.models import MenuItem
from .models import Cart, CartItem

# Create your views here.

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_cart(self, user):
        cart , _ = Cart.objects.get_or_create(customer = user.customer_profile)
        return cart
    
    @action(detail=False,methods=['post'])    
    def add(self,request):
        user = request.user
        menu_item_id = request.data.get('menu_item_id')
        quantity = int(request.data.get('quantity'))
        
        menu_item = get_object_or_404(MenuItem,id=menu_item_id)
        cart = self.get_cart(user)
        
        if cart.restaurant and cart.restaurant != menu_item.category.menu.restaurant:
            return Response({'error': 'Cannot add item from different restaurant'}, status=status.HTTP_400_BAD_REQUEST
            )
        if not cart.restaurant:
            cart.restaurant = menu_item.category.menu.restaurant
            cart.save()
        
        cart_item,created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={
                  'quantity': quantity,
           'price_at_add_time':menu_item.price
        },
            )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return Response({"message:" "Item added in cart successfully"},status=status.HTTP_201_CREATED)
        
    @action(detail=False,methods=['patch'])        
    def update_item(self,request):
        user = request.user
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity'))

        if quantity <=0:
            return Response({'error': 'Quantity cannot be less than or equal to 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(CartItem,id=cart_item_id,
        cart__customer = request.user.customer_profile,
        cart__status = "ACTIVE")
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message":"Cart item updated successfully"},status=status.HTTP_200_OK)
    
    @action(detail=False,methods=['delete'])
    def remove(self,request):
        user = request.user
        cart_item_id = request.data.get('cart_item_id')
        cart_item = get_object_or_404(CartItem,id=cart_item_id,cart__customer = request.user.customer_profile,
        cart__status = "ACTIVE")
        cart_item.delete()
        return Response({"message":"Cart item deleted successfully"},status=status.HTTP_200_OK)
    
    