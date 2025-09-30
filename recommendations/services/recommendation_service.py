from movies.models import MovieDetail
from preferences.models import UserTagPreference

def generate_recommendations(user, limit=10):
    tag_prefs = UserTagPreference.objects.filter(user=user).order_by("-weight")[:5]
    top_tags = [tp.tags for tp in tag_prefs]

    movies = MovieDetail.objects.filter(tags__in=top_tags).distinct().order_by("-popularity")[:limit]

    return movies