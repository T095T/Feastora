from django.shortcuts import render
from rest_framework import status
from .models import Restaurant
from rest_framework.views import APIView
from .serializers import RestaurantDetailSerializer, RestaurantListSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .filters import *

# Create your views here.

class RestaurantListView(APIView):
    permission_classes = [AllowAny]
    filtering_class = RestaurantFilters

    def get(self,request):
        queryset = Restaurant.objects.all()
        serializer = RestaurantListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RestaurantDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk):
        try:
            restaurant = Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantDetailSerializer(instance=restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)