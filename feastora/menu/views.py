from django.contrib.auth import PermissionDenied
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from accounts.permissions import IsRestaurant
from .models import MenuCategory, MenuItem, Menu
from .serializers import (
    MenuCategoryCreateSerializer, MenuCategoryUpdateSerializer, MenuCategoryListSerializer,
    MenuItemCreateSerializer, MenuItemUpdateSerializer,
    MenuItemListSerializer, MenuViewSerializer,
)

# Create your views here.
class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()

    def get_queryset(self):
        user = self.request.user

    #restaurant seeing only there MenuCategories
        if user.is_authenticated and user.is_restaurant:
            return MenuCategory.objects.filter(menu__restaurant=user.restaurant_profile).prefetch_related('items')
        return MenuCategory.objects.all().prefetch_related('items')

    def perform_create(self,serializer):
        user = self.request.user
        if user.is_authenticated and user.is_restaurant:
            menu, _ = Menu.objects.get_or_create(restaurant=user.restaurant_profile)
            serializer.save(menu=menu)
            return
        raise PermissionDenied("Only restaurants can create categories.")

    def perform_update(self, serializer):
        category = self.get_object()
        user = self.request.user
        if category.menu.restaurant != user.restaurant_profile:
            raise PermissionDenied("You cannot edit another restaurant's category.")
        serializer.save()

    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            return [IsAuthenticated(), IsRestaurant()]
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
                category__menu__restaurant=user.restaurant_profile
            ).select_related('category')

        # customers browse by restaurant
        # /api/menu/items/?restaurant_id=1
        restaurant_id = self.request.query_params.get('restaurant_id')
        qs = MenuItem.objects.filter(isAvailable=True).select_related('category')
        if restaurant_id:
            qs = qs.filter(category__menu__restaurant_id=restaurant_id)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsRestaurant()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return MenuItemCreateSerializer
        if self.action in ['update', 'partial_update']:
            return MenuItemUpdateSerializer
        return MenuItemListSerializer


    def perform_create(self,serializer):
        user = self.request.user
        category = serializer.validated_data.get('category')
        if category.menu.restaurant != user.restaurant_profile:
            raise PermissionDenied("Invalid Category")
        serializer.save()

    def perform_update(self, serializer):
        item = self.get_object()
        user = self.request.user
        next_category = serializer.validated_data.get('category', item.category)
        if item.category.menu.restaurant != user.restaurant_profile:
            raise PermissionDenied("You cannot edit another restaurant's item.")
        if next_category.menu.restaurant != user.restaurant_profile:
            raise PermissionDenied("Invalid Category")
        serializer.save()


    def perform_destroy(self, instance):
        # soft delete
        instance.isAvailable = False
        instance.save()



class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        #restaurant seeing only there menu
        if user.is_authenticated and user.is_restaurant:
            return Menu.objects.filter(restaurant=user.restaurant_profile).prefetch_related('categories__items')
        

        #public view
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return Menu.objects.filter(restaurant_id = restaurant_id).prefetch_related('categories__items')
        return Menu.objects.none()

    
    def get_serializer_class(self):
        return MenuViewSerializer