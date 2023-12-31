from django.urls import path

from .views import home_view, delete_url_view, shorts_form_view, short_detail_modal

urlpatterns = [
    path("", home_view, name="dash_home"),
    # path("create/", create_url_view, name="dash_create_url"),
    path("shorts-form/", shorts_form_view, name="dash_shorts_form"),
    path("shorts-detail/<uuid:pk>/", short_detail_modal, name="dash_shorts_detail"),
    path("shorts-detail/<uuid:pk>/qr/", short_detail_modal, name="dash_shorts_qr"),
    # path("settings-menu/", settings_menu, name="settings_menu"),
    path("delete/<uuid:pk>/", delete_url_view, name="dash_delete_url"),
]
