from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.conf import settings


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
            return redirect(settings.POSTS)

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
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect(settings.POSTS)

    if ticket.user != request.user:
        return redirect(settings.POSTS)

    form = TicketForm(instance=ticket)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect(settings.POSTS)

    return render(request, "reviews/ticket_form.html", {"form": form})


@login_required
def ticket_delete(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect(settings.POSTS)

    if ticket.user != request.user:
        return redirect(settings.POSTS)

    if request.method == "POST":
        if ticket.image:
            ticket.image.delete(save=False)
        ticket.delete()

    return redirect(settings.POSTS)
