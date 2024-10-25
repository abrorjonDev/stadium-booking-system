from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.user.models import RoleChoice
from .serializers import UserSerializer


class Register(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def perform_create(self, serializer):
        serializer.save()


class BeOwner(UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(
            updater=self.request.user,
            role=RoleChoice.OWNER
        )
