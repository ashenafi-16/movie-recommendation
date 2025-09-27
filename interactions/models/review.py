import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

from movies.models.movie_reference import MovieReference

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(MovieReference, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    rating = models.ForeignKey("interactions.Rating", null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "interactions_review"
        indexes = [models.Index(fields=['movie', 'user']), models.Index(fields=['created_at'])]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review(user={self.user_id}, movie={self.movie_id})"
    
    