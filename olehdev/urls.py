from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "portfolio/",
        views.portfolio,
        name="portfolio",
    ),

    path(
        "skills/",
        views.skills,
        name="skills",
    ),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "start-project/",
        views.start_project,
        name="start_project",
    ),

    path(
        "client/",
        views.client_dashboard,
        name="client_dashboard",
    ),

    path(
        "client/requests/<int:request_id>/",
        views.client_request_detail,
        name="client_request_detail",
    ),

    path(
        "client/profile/",
        views.client_profile,
        name="client_profile",
    ),

    # ADMIN PANEL
    path(
        "admin-panel/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "admin-panel/requests/",
        views.admin_requests,
        name="admin_requests",
    ),

    path(
        "admin-panel/requests/<int:request_id>/",
        views.admin_request_detail,
        name="admin_request_detail",
    ),

    path(
        "admin-panel/portfolio/add/",
        views.admin_add_project,
        name="admin_add_project",
    ),
    path(
        "admin-panel/skills/add/",
        views.admin_add_skill,
        name="admin_add_skill",
    ),
]
