from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "w-full border-2 border-black px-3 py-2 bg-white"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full border-2 border-black px-3 py-2 bg-white h-32 resize-none",
                    "rows": 5,
                }
            ),
            "image": forms.ClearableFileInput(attrs={"class": "w-full px-3 py-2 bg-white"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]
