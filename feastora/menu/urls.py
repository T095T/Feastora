from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('categories', MenuCategoryViewSet, basename='menu-category')
router.register('items', MenuItemViewSet, basename='menu-item')
router.register('menus', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    
]