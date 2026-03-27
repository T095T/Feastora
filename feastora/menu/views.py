from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import MenuCategory, MenuItem
from .serializers import (
    MenuCategoryCreateSerializer, MenuCategoryUpdateSerializer, MenuCategoryListSerializer,
    MenuItemCreateSerializer, MenuItemUpdateSerializer,
    MenuItemListSerializer,
)

# Create your views here.
class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()

    def get_queryset(self):
        user = self.request.user

    #restaurant seeing only there MenuCategories
        if user.is_authenticated and user.is_restaurant():
            return MenuCategory.objects.filter(restaurant=user.restaurant_profile).prefetch_related('items')

    

    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'list':
            return MenuCategoryListSerializer
        elif self.action == 'create':
            return MenuCategoryCreateSerializer
        elif self.action == 'update':
            return MenuCategoryUpdateSerializer
        return MenuCategoryListSerializer
    
    def destroy(self,request,*args,**kwargs):
        instance = self.get_object()

        # block delete if category has items — deactivate instead
        if instance.items.exists():
            return Response(
                {'detail': 'Cannot delete a category that has menu items. Deactivate it instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
        
    
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.none()

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_restaurant:
            return MenuItem.objects.filter(
                category__restaurant=user.restaurant_profile
            ).select_related('category')

        # customers browse by restaurant
        # /api/menu/items/?restaurant_id=1
        restaurant_id = self.request.query_params.get('restaurant_id')
        qs = MenuItem.objects.filter(isAvailable=True).select_related('category')
        if restaurant_id:
            qs = qs.filter(category__restaurant_id=restaurant_id)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return MenuItemCreateSerializer
        if self.action in ['update', 'partial_update']:
            return MenuItemUpdateSerializer
        return MenuItemListSerializer

    def perform_destroy(self, instance):
        # soft delete
        instance.isAvailable = False
        instance.save()