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