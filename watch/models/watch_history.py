import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

from movies.models.movie_reference import MovieReference

class WatchHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watch_histories")
    movie = models.ForeignKey(MovieReference, on_delete=models.CASCADE, related_name="watch_histories")
    watched_at = models.DateTimeField(default=timezone.now)
    watched_duration = models.PositiveIntegerField(help_text="Duration in seconds", null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField(default=False, help_text="whether the user watched to the end")
    playback_position = models.PositiveIntegerField(null=True, blank=True, help_text="Last know playback position in seconds")

    class Meta:
        db_table = "interactions_watch_history"
        indexes = [
            models.Index(fields=["user", "movie"]),
            models.Index(fields=['movie', 'watched_at']),
        ]
        ordering = ["-watched_at"]        
        def __str__(self):
            return f"watchHistory(user={self.user_id}, movie={self.movie_id}, at={self.watched_at.isoformat()})"
