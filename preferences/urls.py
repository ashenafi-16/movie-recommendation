from rest_framework.routers import DefaultRouter
from .views import UserPreferenceProfileViewSet, UserTagPreferenceViewSet

router = DefaultRouter()
router.register(r'profile', UserPreferenceProfileViewSet, basename="preference-profile")
router.register(r'tags', UserTagPreferenceViewSet, basename='tag-preferences')

urlpatterns = router.urls
