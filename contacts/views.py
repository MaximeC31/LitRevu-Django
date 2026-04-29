from django.shortcuts import render
from .models import Person


def welcome(request):
    return render(request, "contacts/hero.html")


def person_list(request):
    persons = Person.objects.all()
    return render(request, "contacts/person_list.html", {"persons": persons})
