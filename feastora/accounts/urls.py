from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    CustomerRegisterView,
    RestaurantRegisterView,
    RiderRegisterView,
    AdminRegisterView,
    LogoutView,
    
)

urlpatterns = [
    path('register/customer/',   CustomerRegisterView.as_view(),   name='register-customer'),
    path('register/restaurant/', RestaurantRegisterView.as_view(), name='register-restaurant'),
    path('register/rider/',      RiderRegisterView.as_view(),      name='register-rider'),
    path('register/admin/',      AdminRegisterView.as_view(),      name='register-admin'),

    path('login/',         LoginView.as_view(),       name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/',        LogoutView.as_view(),       name='logout'),

    

    
]


