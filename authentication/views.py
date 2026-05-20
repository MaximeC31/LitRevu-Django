from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("reviews:home")

    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reviews:home")

    return render(request, "authentication/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("reviews:home")

    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("reviews:home")

    return render(request, "authentication/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("reviews:home")
