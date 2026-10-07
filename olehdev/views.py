from django.shortcuts import render

from .models import Project


def home(request):
    return render(request, "public/home.html")


def portfolio(request):
    projects = Project.objects.all()

    return render(
        request,
        "public/portfolio.html",
        {
            "projects": projects,
        },
    )
