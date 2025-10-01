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
    list_display = ("id", "user", "movie", "title", "rating", "get_likes_count", "created_at")
    readonly_fields = ("created_at", "updated_at")

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = "Likes Count"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
