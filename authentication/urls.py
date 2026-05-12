from django.urls import path
from . import views

urlpatterns = [
    path("inscription/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
