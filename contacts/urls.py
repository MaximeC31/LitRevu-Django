from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.welcome, name="home"),
    path("contacts/", views.person_list, name="person_list"),
]
