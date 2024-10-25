import uuid
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="%(class)s_creator")
    updater = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updater")
    deleter = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_deleter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
