import uuid

from django.db import models
from django.utils import timezone


class BaseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted_at__isnull=True)


class DeletedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(deleted_at__isnull=False)


class ObjectsWithNoDeletedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).all()


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, db_index=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    objects = BaseManager()
    deleted = DeletedManager()
    all_objects = ObjectsWithNoDeletedManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        super().save(*args, **kwargs)
