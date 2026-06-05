from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("posts/", views.posts_list, name="posts_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path(
        "tickets/<int:ticket_id>/edit/",
        views.ticket_edit,
        name="ticket_edit",
    ),
    path(
        "tickets/<int:ticket_id>/delete/",
        views.ticket_delete,
        name="ticket_delete",
    ),
    path(
        "tickets/<int:ticket_id>/review/",
        views.reviews_add_edit,
        name="reviews_add_edit",
    ),
    path("reviews/create", views.review_create, name="review_create"),
    path(
        "reviews/<int:review_id>/delete/",
        views.review_delete,
        name="review_delete",
    ),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("subscriptions/follow/", views.follow_user, name="follow_user"),
    path(
        "subscriptions/unfollow/",
        views.unfollow_user,
        name="unfollow_user",
    ),
]
