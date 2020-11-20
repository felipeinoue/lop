
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # APIs
    path("api_roles", views.api_roles, name="api_roles"),
    path("api_lops", views.api_lops, name="api_lops"),
    path("api_lop_details/<int:project_id>", views.api_lop_details, name="api_lop_details"),
    path("api_members_add", views.api_members_add, name="api_members_add"),
    path("api_members_table/<int:project_id>", views.api_members_table, name="api_members_table"),
    path("api_profile_details", views.api_profile_details, name="api_profile_details"),
    path("api_profile_username_save", views.api_profile_username_save, name="api_profile_username_save"),
    path("api_profile_email_save", views.api_profile_email_save, name="api_profile_email_save"),
    path("api_profile_password_save", views.api_profile_password_save, name="api_profile_password_save")
]