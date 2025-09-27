from django.core.management.base import BaseCommand
from movies.services.tmdb_sync import sync_movie

class Command(BaseCommand):
    help = "Sync a movie from TMDB by its TMDB ID"
    def add_arguments(self, parser):
        parser.add_argument("tmdb_id", type=int, help="TMDB movie ID to sync")

    def handle(self, *args, **options):
        movie = sync_movie(options['tmdb_id'])
        self.stdout.write(self.style.SUCCESS(f"Movie synced: {movie.title}"))
        