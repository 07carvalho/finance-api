from django.contrib.auth.models import User
from django.db import models
from handlers.managers import BaseModel


class Category(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=False, blank=False)

    class Meta:
        app_label = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
