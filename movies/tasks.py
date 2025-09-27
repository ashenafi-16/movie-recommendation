from celery import shared_task
from .services.tmdb_client import TMDBClient
from .services.tmdb_sync import sync_movie, upsert_movie_from_tmdb

@shared_task
def sync_single_movie_task(tmdb_id: int):
    "Background task to fetch a single movie from TMDB and save it."
    return sync_movie(tmdb_id).id

@shared_task
def sync_popular_movie_task(page: int=1):
    "Background task to fetch a page of popular movies from TMDB and save them all."
    client = TMDBClient()
    data = client.get_popular_movies(page=page)

    synced_ids = []
    for movie_data in data.get("results", []):
        movie = upsert_movie_from_tmdb(movie_data)
        synced_ids.append(movie.id)
    
    return synced_ids