from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from django.views.decorators.http import require_http_methods
from authentication.models import User, UserFollows
from django.db.models import Q
import django.db.models as models


def home(request):
    if request.user.is_authenticated:
        return redirect("reviews:feed")

    return render(request, "home.html")


@login_required
def ticket_create(request):
    form = TicketForm()

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.instance
            ticket.user = request.user
            ticket.save()
            return redirect("reviews:posts_list")

    return render(request, "reviews/ticket_form.html", {"form": form})


@login_required
def posts_list(request):
    tickets = Ticket.objects.filter(user=request.user).annotate(
        post_type=models.Value("ticket")
    )
    reviews = (
        Review.objects.filter(user=request.user)
        .select_related("ticket")
        .annotate(post_type=models.Value("review"))
    )

    posts = [*tickets, *reviews]
    posts.sort(key=lambda post: post.time_created, reverse=True)

    return render(request, "reviews/posts_list.html", {"posts": posts})


@login_required
def ticket_edit(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    except Ticket.DoesNotExist:
        return redirect("reviews:posts_list")

    form = TicketForm(instance=ticket)

    if request.method == "POST":
        old_image = ticket.image.name if ticket.image else None
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            if (
                form.cleaned_data.get("image")
                and old_image
                and old_image != ticket.image.name
            ):
                ticket.image.storage.delete(old_image)
            return redirect("reviews:posts_list")

    return render(request, "reviews/ticket_form.html", {"form": form})


@login_required
@require_http_methods(["POST"])
def ticket_delete(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    except Ticket.DoesNotExist:
        return redirect("reviews:posts_list")

    if ticket.image:
        ticket.image.delete(save=False)
    ticket.delete()

    return redirect("reviews:posts_list")


@login_required
def review_create(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.instance
            ticket.user = request.user
            ticket.save()

            review = review_form.instance
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect("reviews:feed")

    return render(
        request,
        "reviews/review_form.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def reviews_add_edit(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect("reviews:feed")

    existing_review = Review.objects.filter(
        ticket=ticket,
        user=request.user,
    ).first()
    form = ReviewForm(instance=existing_review)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.instance
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("reviews:feed")

    return render(
        request,
        "reviews/review_create_response.html",
        {
            "ticket": ticket,
            "form": form,
        },
    )


@login_required
@require_http_methods(["POST"])
def review_delete(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return redirect("reviews:posts_list")

    review.delete()
    return redirect("reviews:posts_list")


@login_required
def feed(request):
    followed_users = request.user.following.values_list(
        "followed_user",
        flat=True,
    )
    reviewed_ticket = list(
        Review.objects.filter(user=request.user).values_list(
            "ticket",
            flat=True,
        )
    )

    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users)
    ).annotate(post_type=models.Value("ticket"))
    reviews = (
        Review.objects.filter(
            Q(user=request.user) | Q(user__in=followed_users)
        )
        .select_related("user", "ticket", "ticket__user")
        .annotate(post_type=models.Value("review"))
    )

    posts = [*tickets, *reviews]
    posts.sort(key=lambda post: post.time_created, reverse=True)

    return render(
        request,
        "reviews/feed.html",
        {"posts": posts, "reviewed_ticket": reviewed_ticket},
    )


@login_required
def subscriptions(request):
    followed_relations = request.user.following.select_related(
        "followed_user"
    ).order_by("followed_user__username")
    follower_relations = request.user.followed_by.select_related(
        "user"
    ).order_by("user__username")

    return render(request, "reviews/subscriptions.html", locals())


@login_required
@require_http_methods(["POST"])
def follow_user(request):
    username = request.POST.get("username", "").strip()

    if not username:
        messages.error(request, "Nom d'utilisateur requis.")
        return redirect("reviews:subscriptions")

    if username == request.user.username:
        messages.error(request, "Action impossible.")
        return redirect("reviews:subscriptions")

    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("reviews:subscriptions")

    if UserFollows.objects.filter(
        user=request.user,
        followed_user=target_user,
    ).exists():
        messages.error(request, "Déjà suivi.")
        return redirect("reviews:subscriptions")

    UserFollows.objects.create(user=request.user, followed_user=target_user)
    return redirect("reviews:subscriptions")


@login_required
@require_http_methods(["POST"])
def unfollow_user(request):
    user_id = request.POST.get("user_id")

    try:
        follow_relation = UserFollows.objects.get(
            user=request.user,
            followed_user_id=user_id,
        )
    except UserFollows.DoesNotExist:
        messages.error(request, "Abonnement introuvable.")
        return redirect("reviews:subscriptions")

    follow_relation.delete()
    messages.success(request, "Abonnement supprimé.")
    return redirect("reviews:subscriptions")
