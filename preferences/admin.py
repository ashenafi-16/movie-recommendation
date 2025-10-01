from django.contrib import admin
from .models import UserPreferenceProfile, Tag, UserTagPreference


@admin.register(UserPreferenceProfile)
class UserPreferenceProfileAdmin(admin.ModelAdmin):
    list_display = ("preference_id", "user", "interaction_count", "last_update")
    search_fields = ("user__username", "user__email")
    list_filter = ("last_update",)
    ordering = ("-last_update",)
    readonly_fields = ("last_update", "preference_id")

    fieldsets = (
        (None, {
            "fields": ("preference_id", "user", "interaction_count", "last_update")
        }),
        ("Details", {
            "fields": ("preference_embedding", "summary"),
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag_id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("tag_id",)


@admin.register(UserTagPreference)
class UserTagPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user_tag_pref_id", "user", "tag", "weight", "updated_at")
    search_fields = ("user__username", "user__email", "tag__name")
    list_filter = ("updated_at", "tag")
    ordering = ("-updated_at",)
    readonly_fields = ("user_tag_pref_id", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("user_tag_pref_id", "user", "tag", "weight", "updated_at")
        }),
    )
