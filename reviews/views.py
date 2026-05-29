from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from django.views.decorators.http import require_http_methods


def home(request):
    if request.user.is_authenticated:
        return redirect("reviews:feed")

    return render(request, "home.html")


@login_required
def feed(request):
    return render(request, "reviews/feed.html")


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
