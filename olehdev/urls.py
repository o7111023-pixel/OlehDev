from django.urls import path

from .views import home, portfolio


urlpatterns = [
    path("", home, name="home"),
    path("portfolio/", portfolio, name="portfolio"),
]
