from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.bookings.filters import BookingFilter
from apps.bookings.models import Booking, StatusChoice
from apps.bookings.serializers import BookingSerializer
from apps.permissions import HasObjectOwnerPermission, IsOwnerOrAdmin, StadiumOwner
from apps.user.models import RoleChoice


@extend_schema(tags=['Bookings'])
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filterset_class = BookingFilter

    def get_permissions(self):
        if self.action in {'update', 'partial_update', 'destroy'}:
            self.permission_classes = [IsAuthenticated, HasObjectOwnerPermission]
        elif self.action in {'list', 'retrieve'}:
            self.permission_classes = [IsAuthenticated]
        elif self.action in {'cancel', 'confirm'}:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin, StadiumOwner]

        return [perm() for perm in self.permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            self.queryset = Booking.objects.all()
        elif self.request.user.role == RoleChoice.OWNER:
            self.queryset = Booking.objects.filter(
                Q(stadium__creator=self.request.user) |
                Q(creator=self.request.user)
            )
        else:
            self.queryset = Booking.objects.filter(
                creator=self.request.user
            )

        return self.queryset.select_related('stadium', 'creator')

    @extend_schema(
        request={},
        responses={}
    )
    @action(methods=['patch'], url_path='cancel', detail=True)
    def cancel(self, request, *args, **kwargs):
        object = self.get_object()
        object.status = StatusChoice.CANCELLED
        object.updater = request.user
        object.save()
        return Response({"detail": _("Booking Cancelled")})

    @extend_schema(
        request={},
        responses={}
    )
    @action(methods=['patch'], url_path='confirm', detail=True)
    def confirm(self, request, *args, **kwargs):
        object = self.get_object()
        object.status = StatusChoice.CONFIRMED
        object.updater = request.user
        object.save()
        return Response({"detail": _("Booking Confirmed")})

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user,
            status=StatusChoice.PENDING,
        )

    def perform_destroy(self, instance):
        instance.save(
            deleter=self.request.user,
            deleted_at=timezone.now()
        )
