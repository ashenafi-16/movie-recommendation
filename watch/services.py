import logging
from user_agents import parse as parse_user_agent   # pip install pyyaml ua-parser user-agents
from django.utils.timezone import now
from .models import WatchHistory, WatchList
from movies.models.movie_reference import MovieReference as Movie

logger = logging.getLogger(__name__)

def record_watch_event(watch: WatchHistory, request=None):
    """
    Handles logic when a user watches a movie.
    Updates completion status, movie views count, device, and location.
    """

    movie = watch.movie

    if watch.watched_duration and movie.length:
        completion_ratio = watch.watched_duration / movie.length
        completion_threshold = 0.9
        
        if completion_ratio >= completion_threshold:
            watch.completed = True
            watch.save(update_fields=['completed'])
       
    # 2. Increment Movie views_count (only first time)
    if watch.completed:
        Movie.objects.filter(id=movie.id).update(views_count=models.F('views_count') + 1)

    # 3. Extract device_type from request (user agent)
    if request:
        ua_string = request.META.get('HTTP_USER_AGENT', '')
        if ua_string:
            user_agent = parse_user_agent(ua_string)
            watch.device_type = (
                "mobile" if user_agent.is_mobile else
                "tablet" if user_agent.is_tablet else
                "pc" if user_agent.is_pc else
                "other"
            )
            watch.save(update_fields=['device_type'])

    # 4. Extract location (basic = IP address)
    if request:
        ip = get_client_ip(request)
        if ip:
            watch.location = ip   # For simplicity, just save IP (can be extended with geolocation API)
            watch.save(update_fields=['location'])

    logger.info(f"Recorded watch event: User={watch.user.id}, Movie={movie.title}, Completed={watch.completed}")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
