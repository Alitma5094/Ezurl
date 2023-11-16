from django.urls import path

from .views import redirect_url

urlpatterns = [
    path("<str:back_half>/", redirect_url, name="redirect_url"),
]
