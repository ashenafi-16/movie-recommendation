import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

from movies.models.movie_reference import MovieReference

class WatchList(models.Model):
    STATUS_WANT = "want_to_watch"
    STATUS_WATCHING = "watching"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_WANT, "want_to_watch"),
        (STATUS_WATCHING, "watching"),
        (STATUS_COMPLETED, "completed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(MovieReference, on_delete=models.CASCADE, related_name="watchlist_entries")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_WANT)
    priority = models.PositiveSmallIntegerField(default=0, help_text="Optional priority (higher => show earlier)")
    notes = models.TextField(blank=True, default="")
    added_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "interactions_watchlist"
        unique_together = ('user', 'movie')
        indexes = [models.Index(fields=['user', 'status']),models.Index(fields=['movie', 'status'])]
        ordering = ['-added_at']

    def __str__(self):
        return f"WatchList(user={self.user_id}, movie={self.movie_id}, status={self.status})"
