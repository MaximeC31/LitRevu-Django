from django.urls import path

from . import views

urlpatterns = [
    path("fil/", views.feed, name="feed"),
    path("tickets/creer/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:ticket_id>/modifier/", views.ticket_edit, name="ticket_edit"),
    path("tickets/<int:ticket_id>/supprimer/", views.ticket_delete, name="ticket_delete"),
]
