from rest_framework.routers import DefaultRouter
from .views import WatchHistoryViewSet, WatchListViewSet

router = DefaultRouter()
router.register(r'history', WatchHistoryViewSet, basename='watch-history')
router.register(r'list', WatchListViewSet, basename='watch-list')

urlpatterns = router.urls
