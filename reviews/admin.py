from django.contrib import admin
from .models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Review)
