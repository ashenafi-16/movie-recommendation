from django.utils.timezone import now
from movies.models import MovieReference, MovieDetail, Genre, MovieGenre
from .tmdb_client import TMDBClient


def upsert_movie_from_tmdb(data: dict):
    # upsert MovieReference
    movie, _ = MovieReference.objects.update_or_create(
        tmdb_id=data["id"],
        defaults={
            "imdb_id": data.get("imdb_id"),
            "title": data.get("title"),
            "poster_path": data.get("poster_path"),
            "release_date": data.get("release_date") or None,
            "popularity": data.get("popularity", 0.0),
            "last_synced_at": now(),
            "raw": data,
        },
    )

    # upsert MovieDetail
    MovieDetail.objects.update_or_create(
        movie=movie,
        defaults={
            "overview": data.get("overview"),
            "runtime": data.get("runtime"),
            "original_language": data.get("original_language"),
            "vote_average": data.get("vote_average", 0.0),
            "vote_count": data.get("vote_count", 0),
        },
    )

    # upsert Genres and MovieGenre relation
    for g in data.get("genres", []):
        genre, _ = Genre.objects.update_or_create(
            tmdb_genre_id=g["id"],
            defaults={"name": g["name"]},
        )
        MovieGenre.objects.get_or_create(movie=movie, genre=genre)

    return movie


def sync_movie(tmdb_id: int):
    client = TMDBClient()
    data = client.get_movie_detail(tmdb_id)
    return upsert_movie_from_tmdb(data)
