from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.bookings import viewsets

app_name = 'bookings'

router = DefaultRouter()
router.register("bookings", viewsets.BookingViewSet, basename="bookings")

urlpatterns = router.urls