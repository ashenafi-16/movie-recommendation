from django.db.models import Avg, Count
from django.db import transaction

from .models import Rating
from movies.models.movie_reference import MovieReference

def recalc_movie_rating(movie_id):
    movie = MovieReference.objects.select_for_update().get(pk=movie_id)
    agg = Rating.objects.filter(movie_id=movie_id).aggregate(avg=Avg('score'), cnt = Count('id'))
    avg = agg['avg'] or 0.0
    cnt = agg['cnt'] or 0

    # persist atomically
    with transaction.atomic():
        movie.vote_average = float(avg)
        movie.vote_count = int(cnt)
        movie.save(update_fields=['vote_average', 'vote_count'])
        
    