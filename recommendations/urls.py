from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, RecommFeedbackViewSet

router = DefaultRouter()
router.register(r"recommendations", RecommendationViewSet, basename="recommendation")
router.register(r"feedbacks", RecommFeedbackViewSet, basename="feedback")

urlpatterns = router.urls
