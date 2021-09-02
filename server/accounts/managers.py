from django.db import models


class ActivatedAccountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_filed=False)
