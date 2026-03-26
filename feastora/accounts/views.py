from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomerRegistrationSerializer, RestaurantRegisterSerializer, RiderRegisterSerializer,EmailLoginSerializer,AdminRegistrationSerializer
from .models import User, CustomerProfile, RestaurantProfile, RiderProfile
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = EmailLoginSerializer(data=request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({'tokens':tokens},status=status.HTTP_200_OK)


class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Customer Registered Successfully',
            
        }, status=status.HTTP_201_CREATED)

class RestaurantRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RestaurantRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Restaurant Registered Successfully',
            
        }, status=status.HTTP_201_CREATED)
    
class RiderRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RiderRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user   = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Rider Registered Successfully',
            
        }, status=status.HTTP_201_CREATED)

class AdminRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Admin Registered Successfully',
            
        }, status=status.HTTP_201_CREATED)