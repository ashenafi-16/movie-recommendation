from rest_framework import serializers
from django.db import transaction

from .models import Rating, Review, Like
from movies.models.movie_reference import MovieReference

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ('id', 'user', 'movie', 'score', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        movie = data.get('movie')
        if not MovieReference.objects.filter(pk=movie.pk).exists():
            raise serializers.ValidationError("Movie does not exist")
        return data
    
    def create(self, validated_data):
        user = validated_data['user']
        movie = validated_data['movie']
        score = validated_data['score']

        with transaction.atomic():
            rating, created = Rating.objects.update_or_create(
                user=user, movie=movie, defaults={'score': score}
            )
        return rating

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 
            'user',
            'movie',
            'title',
            'content',
            'rating',
            'likes_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at','updated_at','likes_count')
    
    def validate(self, data):
        content = data.get('content', "")
        if not content.strip():
            raise serializers.ValidationError("Review content cannot be empty")
    
        return data

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('id', 'user', 'movie', 'created_at')
    
    def create(self, validated_data):
        like, created = Like.objects.get_or_create(**validated_data)
        return like