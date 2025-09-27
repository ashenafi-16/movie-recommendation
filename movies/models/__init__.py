# movies/models/__init__.py
from .genre import Genre
from .movie_detail import MovieDetail
from .movie_reference import MovieReference
from .movie_genre import MovieGenre

__all__ = ['MovieReference', 'MovieDetail', 'Genre', 'MovieGenre']