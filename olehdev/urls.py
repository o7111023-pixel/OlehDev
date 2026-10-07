from django.urls import path

from .views import (
    admin_dashboard,
    admin_request_detail,
    admin_requests,
    client_dashboard,
    client_profile,
    client_request_detail,
    home,
    login_view,
    logout_view,
    portfolio,
    register,
    skills,
    start_project,
)


urlpatterns = [
    path("", home, name="home"),
    path("portfolio/", portfolio, name="portfolio"),
    path("skills/", skills, name="skills"),
    path("start-project/", start_project, name="start_project"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path(
        "client/",
        client_dashboard,
        name="client_dashboard",
    ),

    path(
        "client/profile/",
        client_profile,
        name="client_profile",
    ),

    path(
        "client/requests/<int:request_id>/",
        client_request_detail,
        name="client_request_detail",
    ),
    path(
        "admin-panel/",
        admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "admin-panel/requests/",
        admin_requests,
        name="admin_requests",
    ),

    path(
        "admin-panel/requests/<int:request_id>/",
        admin_request_detail,
        name="admin_request_detail",
    ),
]
