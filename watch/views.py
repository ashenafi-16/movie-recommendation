from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import WatchHistory, WatchList
from .serializers import WatchHistorySerializer, WatchListSerializer
from interactions.permissions import IsOwnerOrReadOnly
from interactions.views import StandardResultsSetPagination
from .services import record_watch_event


class WatchHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage user's movie watch history.
    """
    serializer_class = WatchHistorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Restrict queryset to the authenticated user's history only."""
        return (
            WatchHistory.objects.filter(user=self.request.user)
            .select_related("movie")
        )

    def perform_create(self, serializer):
        """Save watch history and trigger watch event processing."""
        watch = serializer.save(user=self.request.user)
        record_watch_event(watch, self.request)

    @action(detail=False, methods=["post"], url_path="log")
    def log(self, request):
        """
        Custom action to log a watch event explicitly.
        Equivalent to POST /api/history/ but kept for flexibility.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        watch = serializer.save(user=request.user)
        record_watch_event(watch, request)
        return Response(
            self.get_serializer(watch).data,
            status=status.HTTP_201_CREATED
        )


class WatchListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage user's personal movie watchlist.
    """
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Restrict queryset to the authenticated user's watchlist only."""
        return (
            WatchList.objects.filter(user=self.request.user)
            .select_related("movie")
        )

    def perform_create(self, serializer):
        """Ensure the watchlist entry is tied to the current user."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="toggle/(?P<movie_id>[^/.]+)")
    def toggle(self, request, movie_id=None):
        """
        Toggle movie watchlist status for the current user:
          - Add if not in watchlist
          - Cycle status WANT → WATCHING → COMPLETED
          - Remove if already completed
        """
        entry, created = WatchList.objects.get_or_create(
            user=request.user, movie_id=movie_id
        )

        if created:
            return Response(
                self.get_serializer(entry).data,
                status=status.HTTP_201_CREATED
            )

        if entry.status == WatchList.STATUS_WANT:
            entry.status = WatchList.STATUS_WATCHING
        elif entry.status == WatchList.STATUS_WATCHING:
            entry.status = WatchList.STATUS_COMPLETED
        else:
            entry.delete()
            return Response(
                {"detail": "Removed from watchlist"},
                status=status.HTTP_200_OK
            )

        entry.save(update_fields=["status", "updated_at"])
        return Response(
            self.get_serializer(entry).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"], url_path="movie/(?P<movie_id>[^/.]+)")
    def movie_entry(self, request, movie_id=None):
        """
        Get a specific watchlist entry for the given movie_id.
        """
        entry = WatchList.objects.filter(
            user=request.user, movie_id=movie_id
        ).first()

        if not entry:
            return Response(
                {"detail": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            self.get_serializer(entry).data,
            status=status.HTTP_200_OK
        )
