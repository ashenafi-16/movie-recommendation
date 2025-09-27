from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Rating, Review, Like
from .serializers import RatingSerializer, ReviewSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).select_related('movie')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=["get"], url_path="movie/(?P<movie_id>[^/.]+)")
    def movie_ratings(self, request, movie_id=None):
        ratings = Rating.objests.filter(movie_id=movie_id).select_related('user')
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('movie')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=["get"], url_path="movie/(?P<movie_id>[^/.]+)")
    def movie_reviews(self, request, movie_id=None):
        reviews = Review.objects.filter(movie_id=movie_id).select_related('user')
        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serialzer.data)
    
class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('movie')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=["post"], url_path="toggle/(?P<movie_id>[^/.]+)")
    def toggle_like(self, request, movie_id=None):
        like, created = Like.objects.get_or_create(user=request.user, movie_id=movie_id)

        if not created:
            like.delete()
            return Response({'detail': "Unliked successfully"}, status=status.HTTP_200_OK)
        return Response({'detail': "Liked successfully"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["get"], url_path="movie/(?P<movie_id>[^/.]+)")
    def movie_likes(self, request, movie_id=None):
        likes = Like.objects.filter(movie_id=movie_id).select_related('user')
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)
    
