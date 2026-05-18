from django.urls import path

from . import views

urlpatterns = [
    path("fil/", views.feed, name="feed"),
    path("tickets/creer/", views.ticket_create, name="ticket_create"),
    path("tickets/modifier/<int:ticket_id>/", views.ticket_edit, name="ticket_edit"),
    path("tickets/supprimer/<int:ticket_id>/", views.ticket_delete, name="ticket_delete"),
    path("posts/", views.posts_list, name="posts_list"),
]
