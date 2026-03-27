from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsCustomer(BasePermission):
    message = "Only customers can perform this action."
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_customer
        )


class IsRestaurant(BasePermission):
    message = "Only restaurant accounts can perform this action."
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_restaurant
        )


class IsRider(BasePermission):
    message = "Only riders can perform this action."
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_rider
        )



class IsOwnCustomerProfile(BasePermission):
  
    message = "You can only access your own profile."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_customer
        )

    def has_object_permission(self, request, view, obj):
        # obj is a CustomerProfile instance
        return obj.user == request.user


class IsOwnRestaurantProfile(BasePermission):
    
    message = "You can only access your own restaurant profile."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_restaurant
        )

    def has_object_permission(self, request, view, obj):
       
        return obj.user == request.user


class IsOwnRiderProfile(BasePermission):

    message = "You can only access your own rider profile."

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.is_rider
        )

    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user


class IsOwnProfileOrReadOnly(BasePermission):
    
    message = "You can only edit your own profile."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
       
        if request.method in SAFE_METHODS:
            return True
       
        return obj.user == request.user


class CanViewCustomerProfile(BasePermission):
   
    message = "You do not have permission to view this profile."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        # own profile
        if obj.user == user:
            return True
      
        if request.method in SAFE_METHODS:
            return user.is_restaurant or user.is_rider
       
        return False


class CanViewRestaurantProfile(BasePermission):
    
    message = "You do not have permission to modify this restaurant profile."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # anyone can read
        if request.method in SAFE_METHODS:
            return True
        # only owner can write
        return obj.user == request.user


class CanViewRiderProfile(BasePermission):
   
    message = "You do not have permission to modify this rider profile."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True       # anyone authenticated can read
        return obj.user == request.user  # only owner can write