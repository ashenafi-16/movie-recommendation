from django.contrib import admin
from .models import MovieReference, MovieDetail, Genre, MovieGenre


class MovieGenreInline(admin.TabularInline):
    model = MovieGenre
    extra = 1
    autocomplete_fields = ["genre"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "tmdb_genre_id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(MovieDetail)
class MovieDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "runtime", "original_language", "vote_average", "vote_count")
    search_fields = ("id", "overview")
    list_filter = ("original_language",)
    ordering = ("-vote_average",)


@admin.register(MovieReference)
class MovieReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "tmdb_id", 
        "imdb_id", 
        "title", 
        "release_date", 
        "popularity"
    )
    search_fields = ("title", "imdb_id", "tmdb_id")
    list_filter = ("release_date",)
    ordering = ("-popularity",)
    inlines = [MovieGenreInline]

    fieldsets = (
        (None, {
            "fields": ("tmdb_id", "imdb_id", "title", "poster_path", "release_date", "popularity")
        }),
        ("Extra", {
            "fields": ("detail",),
        }),
    )
