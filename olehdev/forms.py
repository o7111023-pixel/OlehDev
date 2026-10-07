from django import forms

from .models import Message, Profile, ProjectRequest, Skill


class ProjectRequestForm(forms.ModelForm):

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = ProjectRequest

        fields = (
            "name",
            "email",
            "description",
            "skills",
            "budget",
            "deadline",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Project name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "your@email.com",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": (
                        "Briefly describe what you want to build..."
                    ),
                    "rows": 5,
                    "maxlength": 500,
                }
            ),
            "budget": forms.TextInput(
                attrs={
                    "placeholder": "For example: €10–€50",
                }
            ),
            "deadline": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Project name"

        self.fields["description"].help_text = (
            "Maximum 500 characters."
        )

        self.fields["deadline"].label = "Estimated time"

        self.fields["budget"].label = "Budget"


class ProfileForm(forms.Form):

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="First name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
            }
        ),
    )

    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "your@email.com",
            }
        ),
    )

    country = forms.CharField(
        max_length=100,
        required=False,
        label="Country",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Germany",
            }
        ),
    )

    about = forms.CharField(
        max_length=500,
        required=False,
        label="About",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell something about yourself...",
                "rows": 5,
                "maxlength": 500,
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        profile, _ = Profile.objects.get_or_create(
            user=user
        )

        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email
        self.fields["country"].initial = profile.country
        self.fields["about"].initial = profile.about

        self.user = user
        self.profile = profile

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if (
            email
            and self.user.__class__.objects
            .exclude(pk=self.user.pk)
            .filter(email__iexact=email)
            .exists()
        ):
            raise forms.ValidationError(
                "This email is already in use."
            )

        return email

    def save(self):
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]

        self.user.save(
            update_fields=[
                "first_name",
                "last_name",
                "email",
            ]
        )

        self.profile.country = self.cleaned_data["country"]
        self.profile.about = self.cleaned_data["about"]

        self.profile.save(
            update_fields=[
                "country",
                "about",
            ]
        )


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message

        fields = ("text",)

        widgets = {
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Write a message...",
                    "rows": 3,
                }
            ),
        }
