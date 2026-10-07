from django.contrib import admin

from .models import Message, Profile, Project, ProjectRequest, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
    )

    list_filter = (
        "role",
    )

    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "featured",
        "created_at",
    )

    list_filter = (
        "featured",
    )

    search_fields = (
        "title",
        "description",
        "tech_stack",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "order",
    )

    list_filter = (
        "level",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "level",
        "order",
        "name",
    )


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "name",
        "email",
        "description",
    )

    filter_horizontal = (
        "skills",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "project_request",
        "sender",
        "created_at",
    )

    search_fields = (
        "text",
        "sender__username",
    )

    readonly_fields = (
        "created_at",
    )
