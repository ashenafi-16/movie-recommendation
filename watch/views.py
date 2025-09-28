from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import WatchHistory, WatchList
from .serializers import WatchHistorySerializer, WatchListSerializer
from interactions.permissions import IsOwnerOrReadOnly
from interactions.views import StandardResultsSetPagination

class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user).select_related('movie')
    
    def perform_create(self, serializer):
        watch = serializer.save(user=self.request.user)
        record_watch_event(watch)

    @action(detail=False, methods=['post'], url_path='log')
    def log(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        watch = serializer.save(user=request.user)
        record_watch_event(watch)
        return Response(self.get_serializer(watch).data, status=status.HTTP_201_CREATED)
    
class WatchListViewSet(viewsets.ModelViewSet):
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user).select_related('movie')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=["post"], url_path="toggle/(?P<movie_id>[^/.]+)")
    def toggle(self, request, movie_id=None):
        entry, created = WatchList.objects.get_or_create(user=request.user, movie_id=movie_id)

        if created:
            serializer = self.get_serializer(entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        if entry.status == WatchList.STATUS_WANT:
            entry.status = WatchList.STATUS_WATCHING
        elif entry.status == WatchList.STATUS_WATCHING:
            entry.status = WatchList.STATUS_COMPLETED
        else:
            entry.delete()
            return Response({'detail': "Removed from watchlist"}, status=status.HTTP_200_OK)
        entry.save(update_fields=['status', 'updated_at'])
        return Response(self.get_serializer(entry).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"], url_path="movie/(?P<movie_id>[^/.]+)")
    def movie_entry(self, request, movie_id=None):
        entry = WatchList.objects.filter(user=request.user, movie_id=movie_id).first()
        if not entry:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(entry).data, status=status.HTTP_200_OK)