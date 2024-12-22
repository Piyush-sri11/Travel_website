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
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
# Create your views here.


class RegisterViewSet(APIView):
    """
    A view that can accept POST requests with JSON content.
    """

    @extend_schema(request=CustomUserSerializer, responses={201: CustomUserSerializer})
    def post(self,request):
        """
        Create a new user

        Input:
        - email: string
        - password: string
        - first_name: string
        - last_name: string
        
        Output:
        - id: integer

        """
        data=request.data
        serializer=CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    

class LoginViewSet(APIView):

    @extend_schema(request=LoginSerializer)
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')
            user=authenticate(email=email,password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message':'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },status=status.HTTP_200_OK) #return token
            else:
                return Response({'message':'Invalid Credentials'})
        else:
            return Response(serializer.errors)
        
class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    # @extend_schema(request=None, responses={200: None})
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class RegisterAsOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: None})
    def post(self, request):
        user = request.user
        user.is_organizer = True
        user.save()
        return Response({'message': 'You are now registered as an organizer'})
        

class TripOrganizerRegistrationView(APIView):

    @extend_schema(request=TripOrganizerRegistrationSerializer, responses={201: CustomUserSerializer})
    def post(self, request, *args, **kwargs):
        serializer = TripOrganizerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TripViewOrg(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=TripSerializer, responses={200: TripSerializer})
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
    
    
    @extend_schema(request=TripSerializer, responses={200: TripSerializer})
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
    
    @extend_schema(request=TripSerializer, responses={200: TripSerializer})
    def delete(self, request):
        id = request.data.get('id')
        trip = Trip.objects.get(id=id, organizer=request.user)
        trip.delete()
        return Response({"message": "Trip deleted successfully"}, status=status.HTTP_200_OK)
    
    @extend_schema(request=TripSerializer, responses={200: TripSerializer})
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
        
        @extend_schema(request=TripSerializer, responses={200: TripDetailSerializer})
        def get(self,request):
            #only show upcoming trips
            trips = Trip.objects.filter(start_date__gte=datetime.date.today())
            serializer = TripDetailSerializer(trips, many=True)
            return Response(serializer.data)


from .models import Cart, CartItem, Trip
from .serializer import CartSerializer, CartItemSerializer
from .payment_service import PaymentService

class CartViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CartItemSerializer, responses={201: CartItemSerializer})
    def post(self, request):
        data = request.data
        # Check if id and persons are present in the request
        if 'id' not in data or 'persons' not in data:
            return Response({"message": "Please provide trip id and number of persons"}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user)
        trip = Trip.objects.get(id=data['id'])
        cart_item_data = {
            'cart': cart.id,
            'trip': trip.id,
            'persons': data['persons'],
            'total_price': data['persons'] * trip.price
        }
        serializer = CartItemSerializer(data=cart_item_data)
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response({"cart_item_id": cart_item.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(request=None, responses={200: CartSerializer})
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(request=CartItemSerializer)
    def delete(self, request):
        id = request.data.get('id')
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_200_OK)
    
    @extend_schema(request=CartItemSerializer)
    def patch(self, request):
        id = request.data.get('id')
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        data = request.data
        data['total_price'] = data['persons'] * cart_item.trip.price
        serializer = CartItemSerializer(cart_item, data=data, partial=True)
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response({"message": "Cart item updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses={200: None})
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"message": "No items in cart"}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_service = PaymentService()
        # Create a booking for each cart item
        for item in cart_items:
            trip=item.trip
            
            current_date = timezone.now().date()
            
            # Check if current date is before the trip start date
            if current_date >= trip.start_date:
                item.delete()
                return Response({"message": f"Cannot book trip {trip.name} as it has already started."}, status=status.HTTP_400_BAD_REQUEST)
            
            if item.persons > trip.available_slots:
                return Response({"message": "Not enough available slots for trip. Reduce persons or delete the trip" + trip.name}, status=status.HTTP_400_BAD_REQUEST)
            booking = Booking.objects.create(
                trip=item.trip,
                user=request.user,
                total_persons=item.persons,
                total_price=item.total_price,
                status='CONFIRMED'
            )
            # Process payment
            payment = payment_service.process_payment(booking, item.total_price)
            
            if payment.payment_status == 'SUCCESS':
                trip.available_slots -= item.persons
                trip.save()
                item.delete()
            else:
                booking.delete()
                return Response({"message": "Payment failed for trip " + trip.name}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Booking successful for trip to " + trip.name}, status=status.HTTP_200_OK)

class CancelBookingViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=BookingSerializer, responses={200: None})
    def post(self, request):
        booking_id = request.data.get('booking_id')
        booking = Booking.objects.get(id=booking_id, user=request.user)
        trip = booking.trip
        current_date = timezone.now().date()
        if current_date >= trip.start_date:
            return Response({"message": "Cannot cancel booking as trip has already started"}, status=status.HTTP_400_BAD_REQUEST)
        
        trip_date = trip.start_date
        current_date = timezone.now().date()
        days_to_trip = (trip_date - current_date).days

        if days_to_trip >= 15:
            refund_amount = booking.total_price
        elif 7 <= days_to_trip < 15:
            refund_amount = booking.total_price * 0.5
        else:
            refund_amount = 0

        booking.status = 'CANCELLED'
        booking.refund_amount = refund_amount
        booking.save()
        trip.available_slots += booking.total_persons
        trip.save()
        payment_service = PaymentService()
        payment_service.process_refund(booking, refund_amount)
        
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
    
class ViewBookingViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=BookingSerializer, responses={200: BookingSerializer})
    def get(self, request):
        id=request.data.get('booking_id')
        if id:
            booking = Booking.objects.get(id=id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)