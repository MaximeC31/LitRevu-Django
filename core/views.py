from django.shortcuts import redirect, render


def home_view(request):
    if request.user.is_authenticated:
        return redirect("feed")

    return render(request, "home.html")
