from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import MovieReference, Genre
from .serializers import MovieReferenceSerializer, GenreSerializer
from rest_framework import permissions
from movies.tasks import sync_popular_movie_task
from django.conf import settings

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = MovieReference.objects.all().order_by('-popularity')
    serializer_class = MovieReferenceSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', "imdb_id"]
    ordering_fields = ['popularity', 'release_date', 'title']

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        "custom endpoint /movie/by_genre/?genre_id=<uuuid>"

        genre_id = request.query_params.get('genre_id')
        if not genre_id:
            return Response({"error": "genre_id is required"}, status=400)
        
        movies = MovieReference.objects.filter(moviegenre__genre_id=genre_id).order_by('-popularity')
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"] + (["get"] if settings.DEBUG else []))
    def sync_popular(self, request):
        page = int(request.query_params.get("page", 1))
        sync_popular_movie_task.delay(page) # background job
        return Response({"status": "sync started", 'page': page})
    