from django.urls import path

from .views import payments_subscribe, stripe_webhooks, create_portal, create_checkout

urlpatterns = [
    path("manage/", payments_subscribe, name="payments_manage"),
    path("portal/", create_portal, name="payments_portal"),
    path("checkout/", create_checkout, name="payments_checkout"),
    path("webhooks/", stripe_webhooks, name="payments_webhooks"),
]
