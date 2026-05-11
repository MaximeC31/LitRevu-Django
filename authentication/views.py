from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import SignupForm


def signup_view(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    return render(request, "authentication/signup.html", {"form": form})
