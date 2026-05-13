from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm


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
            return redirect("feed")

    return render(request, "reviews/ticket_form.html", {"form": form})


@login_required
def ticket_edit(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect("feed")

    if ticket.user != request.user:
        return redirect("feed")

    form = TicketForm(instance=ticket)

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("feed")

    return render(request, "reviews/ticket_form.html", {"form": form})


@login_required
def ticket_delete(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return redirect("feed")

    if ticket.user != request.user:
        return redirect("feed")

    if request.method == "POST":
        ticket.delete()
        return redirect("feed")

    return render(request, "reviews/ticket_confirm_delete.html", {"ticket": ticket})
