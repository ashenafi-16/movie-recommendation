from rest_framework import serializers
from .models import MovieReference, MovieDetail, Genre, MovieGenre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'tmdb_genre_id', 'name']

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDetail
        fields = ['overview', 'runtime', 'original_language', 'vote_average', 'vote_count']

class MovieReferenceSerializer(serializers.ModelSerializer):
    detail = MovieDetailSerializer(read_only=True)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = MovieReference
        fields = [
            'id',
            'tmdb_id',
            'imdb_id',
            'title',
            'poster_path',
            'release_date',
            'popularity',
            'detail',
            'genres',
        ]
        
    def get_genres(self, obj):
        return [mg.genre.name for mg in obj.moviegenre_set.all()]