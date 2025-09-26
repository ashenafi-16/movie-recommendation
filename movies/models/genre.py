import uuid
from django.db import models 

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmdb_genre_id = models.PositiveIntegerField(unique=True, db_index=True) # keep TMDB id
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "genre"

    def __str__(self):
        return self.name
    