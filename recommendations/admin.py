from django.contrib import admin
from .models import Recommendation, RecommFeedback


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('recom_id', 'user', 'movie', 'generated_at')
    search_fields = ('user__email', 'movie__title')
    list_filter = ('generated_at',)
    readonly_fields = ('recom_id', 'generated_at')


@admin.register(RecommFeedback)
class RecommFeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'user', 'movie', 'action_type', 'timestamp')
    search_fields = ('user__email', 'movie__title')
    list_filter = ('action_type', 'timestamp')
    readonly_fields = ('feedback_id', 'timestamp')
