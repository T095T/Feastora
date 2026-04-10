from django.contrib import admin
from .models import User, CustomerProfile, RiderProfile,AdminProfile
# Register your models here.
admin.site.register(User)
admin.site.register(CustomerProfile)
admin.site.register(RiderProfile)
admin.site.register(AdminProfile)