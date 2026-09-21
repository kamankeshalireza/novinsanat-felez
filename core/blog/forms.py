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
                    "placeholder": "نام و نام خانوادگی خود را وارد کنید",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "id": "email",
                    "placeholder": "آدرس ایمیل خود را وارد کنید",
                    "required": "required",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "id": "website",
                    "placeholder": "وب‌سایت شما (اختیاری)",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "comment",
                    "rows": 5,
                    "placeholder": "نظر خود را بنویسید...",
                    "required": "required",
                }
            ),
            "parent": forms.HiddenInput(),
        }
        labels = {
            "full_name": "نام و نام خانوادگی",
            "email": "آدرس ایمیل",
            "website": "وب‌سایت",
            "comment": "نظر شما",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].required = False
        self.fields["website"].required = False