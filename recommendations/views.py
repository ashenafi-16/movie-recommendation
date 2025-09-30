from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Recommendation, RecommFeedback
from .serializers import RecommendationSerializer, RecommFeedbackSerializer
from .services.recommendation_service import generate_recommendations


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def generate(self, request):
        movies = generate_recommendations(request.user)
        return Response({"recommended_movies": [m.title for m in movies]})


class RecommFeedbackViewSet(viewsets.ModelViewSet):
    queryset = RecommFeedback.objects.all()
    serializer_class = RecommFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
