from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.views.decorators.http import require_http_methods


def home_view(request):
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
    tickets = Ticket.objects.filter(user=request.user)

    posts = []
    for ticket in tickets:
        posts.append(
            {
                "kind": "ticket",
                "ticket": ticket,
                "author": ticket.user.username,
                "title": ticket.title,
                "description": ticket.description,
                "image": ticket.image,
                "time_created": ticket.time_created,
            }
        )
    posts.sort(key=lambda post: post["time_created"], reverse=True)

    return render(request, "reviews/posts_list.html", {"posts": posts})


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
def ticket_delete(request):
    try:
        ticket = Ticket.objects.get(id=request.POST.get("ticket_id"), user=request.user)
    except Ticket.DoesNotExist:
        return redirect("reviews:posts_list")

    if ticket.image:
        ticket.image.delete(save=False)
    ticket.delete()

    return redirect("reviews:posts_list")
