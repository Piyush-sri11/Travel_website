"""
URL configuration for travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from rest_framework import permissions

from trip.views import RegisterViewSet, LoginViewSet, TripOrganizerRegistrationView, TripViewOrg, RegisterAsOrganizerView, LogoutViewSet,TripViewSet, CartViewSet, CheckoutViewSet, CancelBookingViewSet, ViewBookingViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [

    path("admin/", admin.site.urls),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),

    path("register/", RegisterViewSet.as_view(), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
    path("trip/", TripViewSet.as_view(), name="trip"),

    path("logout/", LogoutViewSet.as_view(), name="logout"),
    path("cart/", CartViewSet.as_view(), name="cart"),
    path("checkout/", CheckoutViewSet.as_view(), name="checkout"),
    path("cancel-booking/", CancelBookingViewSet.as_view(), name="cancel-booking"),
    path("view-booking/", ViewBookingViewSet.as_view(), name="view-booking"),
    path("exist-org/", RegisterAsOrganizerView.as_view(), name="existing-user-organizer"),
    path("organizer/register/", TripOrganizerRegistrationView.as_view(), name="organizer-register"),
    path("org-trips/", TripViewOrg.as_view(), name="trip"),
]
