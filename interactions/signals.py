from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models.rating import Rating
from .services import recalc_movie_rating

@receiver(post_save, sender=Rating)
def rating_saved(sender, instance, created, **kwargs):
    recalc_movie_rating(instance.movie_id)

@receiver(post_delete, sender=Rating)
def rating_delete(sender, instance, **kwargs):
    recalc_movie_rating(instance.movie_id)
