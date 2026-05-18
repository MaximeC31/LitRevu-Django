from django.conf import settings
from django.shortcuts import redirect, render


def home_view(request):
    if request.user.is_authenticated:
        return redirect(settings.FLUX)

    return render(request, "home.html")
