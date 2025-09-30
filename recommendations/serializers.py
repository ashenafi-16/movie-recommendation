from rest_framework import serializers
from .models import Recommendation, RecommFeedback
from movies.models import MovieDetail


class RecommendationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(
        queryset=MovieDetail.objects.all()
    )

    class Meta:
        model = Recommendation
        fields = ["recom_id", "user", "movie", "generated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class RecommFeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie = serializers.PrimaryKeyRelatedField(
        queryset=MovieDetail.objects.all()
    )

    class Meta:
        model = RecommFeedback
        fields = ["feedback_id", "user", "movie", "action_type", "timestamp"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
