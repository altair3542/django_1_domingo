from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # apps web
    path("", include("core.urls")),
    path("", include("helpdesk.urls")),

    # api
    path("api/v1/", include(("helpdesk.api.urls", "api"), namespace="api")),

    # auth web tradicional
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
