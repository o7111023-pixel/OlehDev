from django import forms

from .models import ProjectRequest, Skill


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
                    "placeholder": "Your name",
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

        self.fields["description"].help_text = (
            "Maximum 500 characters."
        )

        self.fields["deadline"].label = "Estimated time"

        self.fields["budget"].label = "Budget"
