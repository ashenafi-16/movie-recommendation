import uuid
from django.db import models

class MovieReference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmdb_id = models.PositiveIntegerField(unique=True, db_index=True)
    imdb_id = models.CharField(max_length=32, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=512, db_index=True)
    poster_path = models.CharField(max_length=512, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    popularity = models.FloatField(default=0.0)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    raw = models.JSONField(null=True, blank=True) # raw TMDB paload
    length = models.PositiveIntegerField(null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    class Meta:
        db_table = 'movie_reference'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['popularity']),
        ]
        ordering = ["-popularity"]
    def __str__(self):
        return f"{self.title} ({self.release_date})"
    
    def poster_url(self, size="w500"):
        if not self.poster_path:
            return None
        
        base = "https://image.tmdb.org/t/p"
        return f"{base}/{size}{self.poster_path}"
    