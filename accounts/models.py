from django.contrib.auth.models import AbstractUser
from django.db import models
from shorts.models import Short


class CustomUser(AbstractUser):
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    subscription_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def can_create_custom_url(self):
        if self.subscription_active:
            return True
        short_count = Short.objects.filter(user=self).count()
        if short_count < 3:
            return True
        return False
