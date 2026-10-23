from django.conf import settings
from django.db import models


class Profile(models.Model):

    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        ADMIN = "admin", "Administrator"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    country = models.CharField(
        max_length=100,
        blank=True,
    )

    about = models.TextField(
        max_length=500,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300)

    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )

    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Skill(models.Model):

    class SkillLevel(models.TextChoices):
        CONFIDENT = "confident", "Confident"
        GROWING = "growing", "Good, still growing"
        LEARNING = "learning", "Used, want to learn more"

    name = models.CharField(max_length=100)

    level = models.CharField(
        max_length=20,
        choices=SkillLevel.choices,
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["level", "order", "name"]

    def __str__(self):
        return self.name


class ProjectRequest(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "New"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Deadline(models.TextChoices):
        FIVE_SEVEN_DAYS = "5_7_days", "5–7 days"
        ONE_TWO_WEEKS = "1_2_weeks", "1–2 weeks"
        THREE_FOUR_WEEKS = "3_4_weeks", "3–4 weeks"
        ONE_TWO_MONTHS = "1_2_months", "1–2 months"
        NOT_SURE = "not_sure", "Not sure"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_requests",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    description = models.CharField(
        max_length=500,
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="project_requests",
    )

    budget = models.CharField(
        max_length=100,
        blank=True,
    )

    deadline = models.CharField(
        max_length=20,
        choices=Deadline.choices,
        default=Deadline.NOT_SURE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"


class Message(models.Model):
    project_request = models.ForeignKey(
        ProjectRequest,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message #{self.pk}"
