from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_organizer = models.BooleanField(default=False)  # New field


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Trip(models.Model):
    organizer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organizer')
    name=models.CharField(max_length=100)
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    cancellation_policy = models.TextField()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    persons = models.PositiveIntegerField(default=1,null=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Booking(models.Model):
    trip=models.ForeignKey(Trip, on_delete=models.CASCADE,related_name='bookings')
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='bookings')
    booking_date=models.DateTimeField(auto_now_add=True)
    total_persons=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')])
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    

    def __str__(self):
        return self.trip.name + ' - ' + self.user.username
    
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')])

    def __str__(self):
        return f'Payment for Booking {self.booking.id}'