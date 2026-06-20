from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    """Form for handling contact submissions."""

    class Meta:
        model = Contact
        fields = "__all__"
