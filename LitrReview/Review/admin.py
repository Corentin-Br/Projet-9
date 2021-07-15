from django.contrib import admin

# Register your models here.
from .models import Ticket, Review, UserFollows


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user", "image", "time_created"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["ticket", "rating", "headline", "body", "user"]


@admin.register(UserFollows)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["user", "followed_user"]