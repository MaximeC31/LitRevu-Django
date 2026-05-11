from django.urls import path
from . import views

urlpatterns = [
    path("inscription/", views.signup_view, name="signup"),
]
