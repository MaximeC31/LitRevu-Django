from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmation du mot de passe",
    )
