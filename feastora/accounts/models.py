from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager because we're using email as the unique identifier
    instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',     True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',    True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER   = 'customer',   'Customer'
        RESTAURANT = 'restaurant', 'Restaurant'
        RIDER      = 'rider',      'Rider'
        ADMIN      = 'admin',      'Admin'

    #not using username field
    username   = None
    email      = models.EmailField(unique=True,db_index=True)
    loginPhone = models.CharField(max_length=15, unique=True,db_index=True)
    role       = models.CharField(max_length=20, choices=Role.choices)
    USERNAME_FIELD  = 'email'        # ← login with email
    REQUIRED_FIELDS = ['loginPhone']      # ← required when creating superuser

    objects = UserManager()          # ← plug in custom manager

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    @property
    def is_restaurant(self):
        return self.role == self.Role.RESTAURANT

    @property
    def is_rider(self):
        return self.role == self.Role.RIDER


# ── Role-specific profiles ──────────────────────────────────────────────────
# phone on User is for login
# phone on profiles is the contact number for that role
# they can be different — rider's personal number vs business contact

class CustomerProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    phoneNumber = models.CharField(max_length=15)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)

    def __str__(self):
        return f"Customer: {self.user.email}"


class RestaurantProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    name       = models.CharField(max_length=200)
    address    = models.TextField()
    phoneNumber = models.CharField(max_length=15)    # restaurant contact number
    cuisine    = models.CharField(max_length=100, blank=True)
    isOpen     = models.BooleanField(default=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    speciality = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.name


class RiderProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_number = models.CharField(max_length=20,unique=False)
    isAvailable    = models.BooleanField(default=True)
    avg_rating     = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    phoneNumber    = models.CharField(max_length=15)

    def __str__(self):
        return f"Rider: {self.user.email} {self.phoneNumber}"