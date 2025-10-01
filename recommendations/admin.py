from django.contrib import admin
from .models import Recommendation, RecommFeedback


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "movie", "generated_at", "algorithm_type", "score")
    list_filter = ("generated_at", "algorithm_type")
    search_fields = ("user__username", "movie__title")
    ordering = ("-generated_at",)
    readonly_fields = ("generated_at",)

    fieldsets = (
        (None, {
            "fields": ("user", "movie", "generated_at")
        }),
        ("Details", {
            "fields": ("algorithm_type", "score", "extra_metadata"),
        }),
    )


@admin.register(RecommFeedback)
class RecommFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recomm", "action_type", "timestamp")
    list_filter = ("action_type", "timestamp")
    search_fields = ("user__username", "recomm__id")
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)

    fieldsets = (
        (None, {
            "fields": ("user", "recomm", "action_type", "timestamp")
        }),
        ("Optional Info", {
            "fields": ("extra_notes",),
        }),
    )
