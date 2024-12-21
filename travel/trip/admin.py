# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Trip, Booking, Payment, Cart 

admin.site.register(CustomUser)
admin.site.register(Trip)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Cart)

