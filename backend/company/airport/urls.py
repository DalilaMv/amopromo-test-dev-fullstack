from rest_framework.routers import DefaultRouter
from airport.api.viewsets import *
from django.urls import path, include 
from django.views.decorators.cache import cache_page
from .views import FlightQueryView

router = DefaultRouter()
router.register('domestic-airports', AirportViewSet, basename="domestic-airports"),

urlpatterns = [
    path("flight-query", FlightQueryView.as_view(), name="flight-query"),
]

urlpatterns += router.urls
