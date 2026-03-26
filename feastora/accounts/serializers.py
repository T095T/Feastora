from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, CustomerProfile, RestaurantProfile, RiderProfile,AdminProfile


#Login serializer

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get('email')
        password = data.get('password')

        user =authenticate(request = self.context.get('request'),
        email = email,
        password=password)

        if not user:
            raise serializers.ValidationError('Invalid Email or Password')

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'This account has been deactivated '})
        
        data['user'] = user
        return data

class CustomerRegistrationSerializer(serializers.Serializer):
    email       = serializers.EmailField()
    phoneNumber = serializers.CharField(max_length=15)
    password    = serializers.CharField(write_only=True, min_length=8)
    firstName   = serializers.CharField(max_length=20)
    lastName    = serializers.CharField(max_length=20)
    address     = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        if User.objects.filter(phoneNumber=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


    def create(self, validated_data):
        address = validated_data.pop('address', '')
        phoneNumber = validated_data['phoneNumber']
        user    = User.objects.create_user(
            email       = validated_data['email'],
            phoneNumber = phoneNumber,
            password = validated_data['password'],
            role     = User.Role.CUSTOMER
        )
        CustomerProfile.objects.create(
            user=user,
            phoneNumber=phoneNumber,
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            address=address,
        )
        return user 



class RestaurantRegisterSerializer(serializers.Serializer):
    email            = serializers.EmailField()
    phoneNumber      = serializers.CharField(max_length=15)    # login + restaurant contact phone
    password         = serializers.CharField(write_only=True, min_length=8)
    restaurant_name  = serializers.CharField(max_length=200)
    address          = serializers.CharField()
    cuisine          = serializers.CharField(max_length=100, required=False, allow_blank=True)
    speciality       = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        if User.objects.filter(phoneNumber=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def create(self, validated_data):
        restaurant_name  = validated_data.pop('restaurant_name')
        address          = validated_data.pop('address')
        cuisine          = validated_data.pop('cuisine', '')
        speciality       = validated_data.pop('speciality', '')
        phoneNumber      = validated_data['phoneNumber']

        user = User.objects.create_user(
            email    = validated_data['email'],
            phoneNumber = phoneNumber,
            password = validated_data['password'],
            role     = User.Role.RESTAURANT
        )
        RestaurantProfile.objects.create(
            user    = user,
            name    = restaurant_name,
            phoneNumber = phoneNumber,
            address = address,
            cuisine = cuisine,
            speciality = speciality
        )
        return user


class RiderRegisterSerializer(serializers.Serializer):


    email          = serializers.EmailField()
    phoneNumber    = serializers.CharField(max_length=15)
    password       = serializers.CharField(write_only=True, min_length=8)
    vehicle_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    age            = serializers.IntegerField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        if User.objects.filter(phoneNumber=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate_age(self,value):
        if value<18:
            raise serializers.ValidationError("Rider must be at least 18 years old.")
        return value

    def validate_vehicle_number(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("Vehicle number must contain only alphabets.")
        return value
    
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


    def create(self, validated_data):
        vehicle_number = validated_data.pop('vehicle_number', '')
        phoneNumber = validated_data['phoneNumber']
        age = validated_data['age']
        user = User.objects.create_user(
            email    = validated_data['email'],
            phoneNumber = phoneNumber,
            password = validated_data['password'],
            role     = User.Role.RIDER
        )
        RiderProfile.objects.create(
            user=user,
            vehicle_number=vehicle_number,
            phoneNumber=phoneNumber,
            age=age,
        )
        return user

class AdminRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phoneNumber = serializers.CharField(max_length=15)
    firstName = serializers.CharField(max_length=20)
    lastName = serializers.CharField(max_length=20)
    address = serializers.CharField()
    isActive = serializers.BooleanField(default=True)
    isVerified = serializers.BooleanField(default=False)




    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_phoneNumber(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone must contain digits only.")
        if User.objects.filter(phoneNumber=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    def validate_age(self,value):
        if value<18:
            raise serializers.ValidationError("Rider must be at least 18 years old.")
        return value

    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def validate_active(self,value):
        if value is False:
            raise serializers.ValidationError("Admin must be active.")
        return value
    
    def validate_verified(self,value):
        # Admin can be created unverified; verification can happen later.
        return value


    def create(self, validated_data):
        phoneNumber = validated_data['phoneNumber']
        user = User.objects.create_user(
            email    = validated_data['email'],
            phoneNumber = phoneNumber,
            password = validated_data['password'],
            role     = User.Role.ADMIN
        )
        AdminProfile.objects.create(
            user=user,
            phoneNumber=phoneNumber,
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            address=validated_data['address'],
            isActive=validated_data.get('isActive', True),
            isVerified=validated_data.get('isVerified', False),
        )
        return user

#Logout 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)