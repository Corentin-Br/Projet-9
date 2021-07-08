from django.contrib import admin

# Register your models here.
from .models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "image", "time_created"]

@admin.register(Review)
class TicketAdming(admin.ModelAdmin):
    list_display = ["ticket", "rating", "headline", "body"]