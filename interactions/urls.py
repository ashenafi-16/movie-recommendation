from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RatingViewSet, ReviewViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = router.urls

