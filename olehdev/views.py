from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectRequestForm
from .models import Project, ProjectRequest, Skill


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


def skills(request):
    skills = Skill.objects.all()

    return render(
        request,
        "public/skills.html",
        {
            "skills": skills,
        },
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("client_dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("client_dashboard")

    else:
        form = UserCreationForm()

    return render(
        request,
        "public/register.html",
        {
            "form": form,
        },
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("client_dashboard")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("client_dashboard")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "public/login.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):
    logout(request)

    return redirect("home")


@login_required
def start_project(request):

    if request.method == "POST":
        form = ProjectRequestForm(request.POST)

        if form.is_valid():
            project_request = form.save(commit=False)

            project_request.user = request.user

            project_request.save()

            form.save_m2m()

            return redirect(
                "client_request_detail",
                request_id=project_request.id,
            )

    else:
        form = ProjectRequestForm(
            initial={
                "name": request.user.get_full_name(),
                "email": request.user.email,
            }
        )

    return render(
        request,
        "public/start_project.html",
        {
            "form": form,
        },
    )


@login_required
def client_dashboard(request):
    requests = ProjectRequest.objects.filter(
        user=request.user,
    )

    return render(
        request,
        "client/dashboard.html",
        {
            "requests": requests,
        },
    )


@login_required
def client_request_detail(request, request_id):
    project_request = get_object_or_404(
        ProjectRequest,
        id=request_id,
        user=request.user,
    )

    return render(
        request,
        "client/request_detail.html",
        {
            "project_request": project_request,
        },
    )

@login_required
def client_profile(request):
    return render(
        request,
        "client/profile.html",
    )

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.is_staff:
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def admin_dashboard(request):
    requests = ProjectRequest.objects.all()

    new_count = requests.filter(
        status=ProjectRequest.Status.NEW,
    ).count()

    accepted_count = requests.filter(
        status=ProjectRequest.Status.ACCEPTED,
    ).count()

    completed_count = requests.filter(
        status=ProjectRequest.Status.COMPLETED,
    ).count()

    rejected_count = requests.filter(
        status=ProjectRequest.Status.REJECTED,
    ).count()

    return render(
        request,
        "admin/dashboard.html",
        {
            "requests": requests[:10],
            "new_count": new_count,
            "accepted_count": accepted_count,
            "completed_count": completed_count,
            "rejected_count": rejected_count,
        },
    )


@admin_required
def admin_requests(request):
    requests = ProjectRequest.objects.all()

    return render(
        request,
        "admin/requests.html",
        {
            "requests": requests,
        },
    )


@admin_required
def admin_request_detail(request, request_id):
    project_request = get_object_or_404(
        ProjectRequest,
        id=request_id,
    )

    if request.method == "POST":

        status = request.POST.get("status")

        valid_statuses = {
            choice[0]
            for choice in ProjectRequest.Status.choices
        }

        if status in valid_statuses:
            project_request.status = status
            project_request.save()

            messages.success(
                request,
                "Request status updated.",
            )

        return redirect(
            "admin_request_detail",
            request_id=project_request.id,
        )

    return render(
        request,
        "admin/request_detail.html",
        {
            "project_request": project_request,
        },
    )
