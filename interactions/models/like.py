import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from movies.models.movie_reference import MovieReference


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    movie = models.ForeignKey(MovieReference, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'interactions_like'
        unique_together = ('user', 'movie')
        indexes = [models.Index(fields=['movie', 'user'])]

    def __str__(self):
        return f"Like(user={self.user_id}, movie={self.movie_id})"