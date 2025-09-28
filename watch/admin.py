# interactions/admin.py
from django.contrib import admin
from .models import WatchHistory, WatchList  # adjust import if models in module

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "watched_at", "watched_duration", "completed")
    search_fields = ("user__username", "movie__title")
    list_filter = ("device_type", "completed")

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "status", "added_at")
    search_fields = ("user__username", "movie__title")
    list_filter = ("status",)
