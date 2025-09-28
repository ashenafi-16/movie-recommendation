from rest_framework import serializers
from .models import WatchHistory, WatchList
from movies.models.movie_reference import MovieReference

class WatchHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    movie_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WatchHistory
        fields = (
            "id", "user", "movie", "movie_detail", "watched_at",
            "watched_duration", "device_type", "location",
            "completed", "playback_position",
        )
        read_only_fields = ("id", "watched_at")

    def get_movie_detail(self, obj):
        return {'id': obj.movie_id, "title": getattr(obj.movie, 'title', None)}
    
class WatchListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    movie_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WatchList
        fields = (
            "id", "user", "movie", "movie_detail", "status", 
            "priority", "notes", "added_at", "updated_at"
        )
        read_only_fields = ("id", "added_at", "updated_at")

    def get_movie_detail(self, obj):
        return {'id': obj.movie_id, 'title': getattr(obj.movie, 'title', None)}
    
