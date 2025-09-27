import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from movies.models.movie_reference import MovieReference

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    movie = models.ForeignKey(MovieReference, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interactions_rating'
        unique_together = ('user', 'movie')
        indexes = [models.Index(fields=['movie', 'user']), models.Index(fields=['movie', 'score'])]
        ordering = ['-updated_at']

    def __str__(self):
        return f"Rating(User={self.user_id}, movie={self.movie_id}, score={self.score})"
