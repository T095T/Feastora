from django.urls import path
from .views import RestaurantDetailView, RestaurantListView

urlpatterns = [
    path('', RestaurantListView.as_view()),
    path("<int:pk>/", RestaurantDetailView.as_view()),
]