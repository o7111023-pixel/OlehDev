from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    MessageForm,
    ProfileForm,
    ProjectForm,
    ProjectRequestForm,
    SkillForm,
)
from .models import Message, Project, ProjectRequest, Skill


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
    confident_skills = Skill.objects.filter(
        level=Skill.SkillLevel.CONFIDENT
    )

    growing_skills = Skill.objects.filter(
        level=Skill.SkillLevel.GROWING
    )

    learning_skills = Skill.objects.filter(
        level=Skill.SkillLevel.LEARNING
    )

    return render(
        request,
        "public/skills.html",
        {
            "confident_skills": confident_skills,
            "growing_skills": growing_skills,
            "learning_skills": learning_skills,
        },
    )


def register(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")

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
        if request.user.is_staff:
            return redirect("admin_dashboard")

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

            if user.is_staff:
                return redirect("admin_dashboard")

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
        form = ProjectRequestForm()

    return render(
        request,
        "client/start_project.html",
        {
            "form": form,
        },
    )


@login_required
def client_dashboard(request):
    requests = ProjectRequest.objects.filter(
        user=request.user
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
        ProjectRequest.objects.prefetch_related(
            "skills",
            "messages__sender",
        ),
        id=request_id,
        user=request.user,
    )

    if request.method == "POST":
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)

            message.project_request = project_request
            message.sender = request.user

            message.save()

            return redirect(
                "client_request_detail",
                request_id=project_request.id,
            )

    else:
        message_form = MessageForm()

    chat_messages = project_request.messages.select_related(
        "sender"
    ).all()

    return render(
        request,
        "client/request_detail.html",
        {
            "project_request": project_request,
            "chat_messages": chat_messages,
            "message_form": message_form,
        },
    )


@login_required
@require_POST
def client_cancel_request(request, request_id):
    project_request = get_object_or_404(
        ProjectRequest,
        id=request_id,
        user=request.user,
    )

    if project_request.status in {
        ProjectRequest.Status.COMPLETED,
        ProjectRequest.Status.REJECTED,
        ProjectRequest.Status.CANCELLED,
    }:
        messages.error(
            request,
            "This request cannot be cancelled.",
        )
    else:
        project_request.status = ProjectRequest.Status.CANCELLED
        project_request.save(update_fields=["status", "updated_at"])

        messages.success(
            request,
            "Your project request has been cancelled.",
        )

    return redirect(
        "client_request_detail",
        request_id=project_request.id,
    )


@login_required
def client_profile(request):
    user_requests = ProjectRequest.objects.filter(
        user=request.user
    )

    total_requests = user_requests.count()

    completed_requests = user_requests.filter(
        status=ProjectRequest.Status.COMPLETED
    ).count()

    active_requests = user_requests.exclude(
        status__in=[
            ProjectRequest.Status.COMPLETED,
            ProjectRequest.Status.REJECTED,
        ]
    ).count()

    if request.method == "POST":
        profile_form = ProfileForm(
            request.user,
            request.POST,
        )

        if profile_form.is_valid():
            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("client_profile")

    else:
        profile_form = ProfileForm(
            request.user,
        )

    return render(
        request,
        "client/profile.html",
        {
            "profile_form": profile_form,
            "total_requests": total_requests,
            "completed_requests": completed_requests,
            "active_requests": active_requests,
        },
    )


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.is_staff:
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
@require_POST
def admin_delete_request(request, request_id):
    project_request = get_object_or_404(
        ProjectRequest,
        id=request_id,
    )

    project_request.delete()

    messages.success(
        request,
        "Project request and its messages were deleted.",
    )

    return redirect("admin_requests")


@admin_required
def admin_dashboard(request):
    requests = ProjectRequest.objects.all()

    new_count = requests.filter(
        status=ProjectRequest.Status.NEW
    ).count()

    accepted_count = requests.filter(
        status=ProjectRequest.Status.ACCEPTED
    ).count()

    completed_count = requests.filter(
        status=ProjectRequest.Status.COMPLETED
    ).count()

    rejected_count = requests.filter(
        status=ProjectRequest.Status.REJECTED
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
        ProjectRequest.objects.prefetch_related(
            "skills",
            "messages__sender",
        ),
        id=request_id,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "status":
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

        if action == "message":
            message_form = MessageForm(request.POST)

            if message_form.is_valid():
                message = message_form.save(commit=False)

                message.project_request = project_request
                message.sender = request.user

                message.save()

                return redirect(
                    "admin_request_detail",
                    request_id=project_request.id,
                )

        else:
            message_form = MessageForm()

    else:
        message_form = MessageForm()

    chat_messages = project_request.messages.select_related(
        "sender"
    ).all()

    return render(
        request,
        "admin/request_detail.html",
        {
            "project_request": project_request,
            "chat_messages": chat_messages,
            "message_form": message_form,
        },
    )


@admin_required
def admin_add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            messages.success(
                request,
                f'Project "{project.title}" added successfully.',
            )

            return redirect("portfolio")

    else:
        form = ProjectForm()

    return render(
        request,
        "admin/project_form.html",
        {
            "form": form,
        },
    )


@admin_required
def admin_add_skill(request):
    level = request.GET.get("level")

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save()

            messages.success(
                request,
                f'Skill "{skill.name}" added successfully.',
            )

            return redirect("skills")

    else:
        form = SkillForm(
            initial={
                "level": (
                    level
                    if level in {
                        choice[0]
                        for choice in Skill.SkillLevel.choices
                    }
                    else Skill.SkillLevel.GROWING
                ),
            }
        )

    return render(
        request,
        "admin/skill_form.html",
        {
            "form": form,
        },
    )
