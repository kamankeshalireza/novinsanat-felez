from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "email", "website", "comment", "parent"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "name",
                    "placeholder": "Enter your full name",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "id": "email",
                    "placeholder": "Enter your email address",
                    "required": "required",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "id": "website",
                    "placeholder": "Your website (optional)",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "comment",
                    "rows": 5,
                    "placeholder": "Write your thoughts here...",
                    "required": "required",
                }
            ),
            "parent": forms.HiddenInput(),
        }
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "website": "Website",
            "comment": "Your Comment",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].required = False
        self.fields["website"].required = False
