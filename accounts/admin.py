from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', "subscription_active"]
    fieldsets = UserAdmin.fieldsets + (
        ("Subscription", {'fields': ('stripe_customer_id', 'subscription_active')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)