from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    subscription_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email
