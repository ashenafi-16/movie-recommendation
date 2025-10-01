from django.contrib import admin
from .models import Rating, Review, Like


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "score", "created_at", "updated_at")
    list_filter = ("score", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ("user", "movie", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "title", "rating", "likes_count", "created_at")
    list_filter = ("created_at", "updated_at", "rating")
    search_fields = ("user__username", "user__email", "movie__title", "title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "likes_count")

    inlines = [LikeInline]

    fieldsets = (
        (None, {
            "fields": ("user", "movie", "title", "content", "rating")
        }),
        ("Metadata", {
            "fields": ("likes_count", "created_at", "updated_at"),
        }),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
