from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("feed/", views.feed, name="feed"),
    path("posts/", views.posts_list, name="posts_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/update/<int:ticket_id>/", views.ticket_edit, name="ticket_edit"),
    path("tickets/delete/", views.ticket_delete, name="ticket_delete"),
]
