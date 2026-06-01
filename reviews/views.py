from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from django.views.decorators.http import require_http_methods
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
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    reviews = Review.objects.filter(user=request.user).order_by("-time_created")
    return render(request, "reviews/posts_list.html", locals())


@login_required
def ticket_edit(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    except Ticket.DoesNotExist:
        return redirect("reviews:posts_list")

    form = TicketForm(instance=ticket)

    if request.method == "POST":
        old_image = ticket.image
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            if form.cleaned_data.get("image") and old_image:
                old_image.delete(save=False)
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
        request, "reviews/review_form.html", {"ticket_form": ticket_form, "review_form": review_form}
    )


@login_required
def reviews_add_edit(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect("reviews:feed")

    existing_review = Review.objects.filter(ticket=ticket, user=request.user).first()
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
    followed_user_ids = request.user.following.values_list("followed_user_id", flat=True)

    user_tickets = Ticket.objects.filter(user=request.user)
    followed_tickets = Ticket.objects.filter(user_id__in=followed_user_ids)
    visible_tickets = user_tickets | followed_tickets

    user_reviews = Review.objects.filter(user=request.user)
    followed_reviews = Review.objects.filter(user_id__in=followed_user_ids)
    ticket_reviews = Review.objects.filter(ticket__user=request.user)
    visible_reviews = user_reviews | followed_reviews | ticket_reviews

    visible_tickets = visible_tickets.annotate(
        content_type=models.Value("TICKET", output_field=models.CharField())
    )
    visible_reviews = visible_reviews.annotate(
        content_type=models.Value("REVIEW", output_field=models.CharField())
    )

    reviewed_ticket_ids = list(Review.objects.filter(user=request.user).values_list("ticket_id", flat=True))

    posts = sorted(
        list(visible_tickets) + list(visible_reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "reviews/feed.html", locals())
