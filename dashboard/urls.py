from django.urls import path

from .views import home_view, delete_url_view, shorts_form_view, short_detail_modal, payments_subscribe, \
    stripe_webhooks, customer_portal

urlpatterns = [
    path("", home_view, name="dash_home"),
    path("payments/", payments_subscribe, name="dash_payments"),
    path("payments/portal/", customer_portal, name="dash_stripe_portal"),
    path("payments/webhooks/", stripe_webhooks, name="dash_webhooks"),
    path("shorts-form/", shorts_form_view, name="dash_shorts_form"),
    path("shorts-detail/<uuid:pk>/", short_detail_modal, name="dash_shorts_detail"),
    path("shorts-detail/<uuid:pk>/qr/", short_detail_modal, name="dash_shorts_qr"),
    path("delete/<uuid:pk>/", delete_url_view, name="dash_delete_url"),
]
