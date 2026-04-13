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
    phoneNumber = models.CharField(max_length=15, unique=True,db_index=True)
    role       = models.CharField(max_length=20, choices=Role.choices)
    USERNAME_FIELD  = 'email'        # ← login with email
    REQUIRED_FIELDS = ['phoneNumber']      # ← required when creating superuser

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
# phoneNumber on User is for login
# phoneNumber on profiles is the contact number for that role
# they can be different — rider's personal number vs business contact


class BaseProfile(models.Model):
    phoneNumber = models.CharField(max_length=15)
    firstName   = models.CharField(max_length=20)
    lastName    = models.CharField(max_length=20)
    address     = models.TextField(blank=True)

    class Meta:
        abstract = True

class CustomerProfile(BaseProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    def __str__(self):
        return f"Customer: {self.user.email} "

class AdminProfile(BaseProfile):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    isActive   = models.BooleanField(default=True)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return f"Admin: {self.user.email} {self.phoneNumber}"

class RiderProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_number = models.CharField(max_length=20,unique=True)
    isAvailable    = models.BooleanField(default=True)
    avg_rating     = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    phoneNumber    = models.CharField(max_length=15)
    age            = models.IntegerField()
    isDisabled     = models.BooleanField(default=False)
    isVerified     = models.BooleanField(default=False)

    def __str__(self):
        return f"Rider: {self.user.email} {self.vehicle_number}"

