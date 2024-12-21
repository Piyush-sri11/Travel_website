from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Trip, Booking, Payment, CustomUser, Cart
import datetime
from rest_framework.exceptions import ValidationError
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_organizer = validated_data.get('is_organizer', instance.is_organizer)
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField()




class TripOrganizerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'is_organizer']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['is_organizer'] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user




class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        exclude = ['organizer','cancellation_policy']

    def vaidate_start_date(self, start_date):
        if start_date < datetime.date.today():
            raise serializers.ValidationError("Start date should be greater than today")
        return start_date
    
    def validate_end_date(self, end_date):
        start_date = self.initial_data.get('start_date')
        if start_date and end_date < datetime.datetime.strptime(start_date, '%Y-%m-%d').date():
            raise serializers.ValidationError("End date should be greater than start date")
        return end_date

    def create(self, validated_data):
        trip = Trip.objects.create(**validated_data)
        return trip
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.price = validated_data.get('price', instance.price)
        instance.total_slots = validated_data.get('total_slots', instance.total_slots)
        instance.available_slots = validated_data.get('available_slots', instance.available_slots)
        instance.cancellation_policy = validated_data.get('cancellation_policy', instance.cancellation_policy)
        instance.save()
        return instance

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']

class TripDetailSerializer(serializers.ModelSerializer):
    #all fields of trip must be read only
    organizer = OrganizerSerializer()
    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['organizer', 'name', 'description', 'start_date', 'end_date', 'price', 'total_slots', 'available_slots', 'cancellation_policy']

class CartSerializer(serializers.ModelSerializer):
    trip_name = serializers.CharField(source='trip.name', read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'
        extra_fields = ['trip_name']

    def validate_persons(self, persons):
        if persons <= 0:
            raise serializers.ValidationError("Persons should be greater than 0")
        return persons
    
    def create(self, validated_data):
        trip = validated_data.get('trip')
        if trip.available_slots < validated_data.get('persons'):
            raise serializers.ValidationError("Not enough available slots")
        cart = Cart.objects.create(**validated_data)
        # trip.available_slots -= validated_data.get('persons')
        # trip.save()
        return cart
    
    def update(self, instance, validated_data):
        trip = instance.trip
        if trip.available_slots + instance.persons < validated_data.get('persons'):
            raise serializers.ValidationError("Not enough available slots")
        # trip.available_slots += instance.persons
        # trip.available_slots -= validated_data.get('persons')
        # trip.save()
        instance.persons = validated_data.get('persons', instance.persons)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        return instance
    

    
        

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Payment
        fields = '__all__'