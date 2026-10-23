from catalog.models import Newspaper
from django import forms


class NewsForm(forms.ModelForm):

  class Meta:
    model = Newspaper
    fields = ["title", "content", "topic", "publishers"]
    widgets = {
        "title": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter title"}
        ),
        "content": forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter news content",
            }
        ),
        "topic": forms.Select(attrs={"class": "form-select"}),
        "publishers": forms.SelectMultiple(
            attrs={"class": "form-select", "size": 4}
        ),
    }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "name", "placeholder": "Enter your name..."})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Enter your email..."})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "id": "message", "placeholder": "Enter your message here...", "style": "height: 12rem"})
    )