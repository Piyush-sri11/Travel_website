from django.shortcuts import render
from rest_framework import viewsets
from .models import Trip, Booking, Payment
from .serializer import TripSerializer, BookingSerializer, PaymentSerializer, LoginSerializer, CustomUserSerializer,TripOrganizerRegistrationSerializer
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
# Create your views here.


class RegisterViewSet(APIView):
    def post(self,request):
        data=request.data
        serializer=CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    

class LoginViewSet(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')
            user=authenticate(email=email,password=password)
            if user:
                token,created=Token.objects.get_or_create(user=user)
                return Response({'message':'Login Successful','token':token.key}) #return token
            else:
                return Response({'message':'Invalid Credentials'})
        else:
            return Response(serializer.errors)
        
class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class RegisterAsOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_organizer = True
        user.save()
        return Response({'message': 'You are now registered as an organizer'})
        

class TripOrganizerRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TripOrganizerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TripViewOrg(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_organizer:
            return Response({"detail": "Only organizers can add new trips."}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            trip = serializer.save(organizer=request.user)
            return Response({"trip_id": trip.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def get(self,request):
        data=request.data
        id=data.get('id')
        if id:
            try:
                trip = Trip.objects.get(id=id, organizer=request.user)
                serializer = TripSerializer(trip)
                return Response(serializer.data)
            except Trip.DoesNotExist:
                return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            trips = Trip.objects.filter(organizer=request.user)
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data)
    
          
    def delete(self, request):
        id = request.data.get('id')
        trip = Trip.objects.get(id=id, organizer=request.user)
        trip.delete()
        return Response({"message": "Trip deleted successfully"}, status=status.HTTP_200_OK)
    
    def patch(self, request):
        id = request.data.get('id')
        trip = Trip.objects.get(id=id, organizer=request.user)
        data = request.data
        serializer = TripSerializer(trip, data=data, partial=True)
        if serializer.is_valid():
            trip = serializer.save()
            return Response({"trip_id": trip.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
import datetime
from .serializer import TripDetailSerializer,CartSerializer
from .models import Cart

class TripViewSet(APIView):
        
        def get(self,request):
            #only show upcoming trips
            trips = Trip.objects.filter(start_date__gte=datetime.date.today())
            serializer = TripDetailSerializer(trips, many=True)
            return Response(serializer.data)

class CartViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        # Check if id and persons are present in the request
        if 'id' not in data or 'persons' not in data:
            return Response({"message": "Please provide trip id and number of persons"}, status=status.HTTP_400_BAD_REQUEST)

        data['user'] = request.user.id  # Pass the user id instead of the user instance
        id = data.pop('id')
        trip = Trip.objects.get(id=id)
        data['trip'] = trip.id  # Pass the trip id instead of the trip instance
        data['total_price'] = data['persons'] * trip.price
        print("Request data:", data)
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            cart = serializer.save()
            return Response({"cart_id": cart.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        carts = Cart.objects.filter(user=request.user)
        print(carts)
        serializer = CartSerializer(carts, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
    def delete(self, request):
        id = request.data.get('id')
        cart = Cart.objects.get(id=id, user=request.user)
        cart.delete()
        return Response({"message": "Cart deleted successfully"}, status=status.HTTP_200_OK)
    
    def patch(self, request):
        id = request.data.get('id')
        cart = Cart.objects.get(id=id, user=request.user)
        data = request.data
        serializer = CartSerializer(cart, data=data, partial=True)
        if serializer.is_valid():
            cart = serializer.save()
            return Response({"cart_id": cart.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BookingViewSet(APIView):
    
    def get(self,request,id):
        queryset = Booking.objects.filter(trip=id)
        serializer = BookingSerializer(queryset, many=True)

        return Response(serializer.data)