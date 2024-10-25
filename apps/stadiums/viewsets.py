from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.stadiums.models import Stadium, Image
from apps.stadiums.serializers import StadiumSerializer, ImageSerializer
from apps.permissions import IsOwnerOrAdmin, HasObjectOwnerPermission
from apps.user.models import RoleChoice


class PermissionsMixin:
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in {'retrieve', 'list'}:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated, HasObjectOwnerPermission]
        return [perm() for perm in self.permission_classes]


class PerformActionsMixin:
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        self.request.user.role = RoleChoice.OWNER
        self.request.user.save(update_fields=['role'])

    def perform_update(self, serializer):
        serializer.save(updater=self.request.user)

    def perform_destroy(self, instance):
        instance.deleter=self.request.user
        instance.save()



@extend_schema(
    request=StadiumSerializer,
    responses={200: StadiumSerializer()},
    tags=['Stadiums'])
class StadiumViewSet(PermissionsMixin, PerformActionsMixin, ModelViewSet):
    serializer_class = StadiumSerializer
    filterset_fields = {
        'name': ['icontains'],
        'address': ['icontains'],
        'creator': ['exact'], # for Admin only
    }

    def get_queryset(self):
        user = self.request.user
        if user.role == RoleChoice.OWNER:
            queryset = Stadium.objects.filter(creator=user, deleter__isnull=True)
        else:
            queryset = Stadium.objects.all()
        return queryset.prefetch_related('images')


@extend_schema(
    request=ImageSerializer,
    responses={200: ImageSerializer()},
    tags=['Stadiums'])
class ImageViewSet(PermissionsMixin, PerformActionsMixin, ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
