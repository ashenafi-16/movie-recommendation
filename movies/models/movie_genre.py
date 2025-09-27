import uuid
from django.db import models

class MovieGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey("movies.MovieReference", on_delete=models.CASCADE)
    genre = models.ForeignKey('movies.Genre', on_delete=models.CASCADE)
