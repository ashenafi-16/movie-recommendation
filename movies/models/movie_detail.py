import uuid
from django.db import models

class MovieDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.OneToOneField("movies.MovieReference", on_delete=models.CASCADE, related_name="detail")
    overview = models.TextField(null=True, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)
    original_language = models.CharField(max_length=8, null=True)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "movie_detail"

    def __str__(self):
        return f"Detail for {self.movie.title}"