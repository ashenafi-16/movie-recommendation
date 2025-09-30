from django.db.models.signals import post_save
from django.dispatch import receiver
from watch.models import WatchHistory
from recommendations.models import RecommFeedback
from .services.tag_service import update_tag_weight

@receiver(post_save, sender=WatchHistory)
def update_preferences_from_watch(sender, instance, created, **kwargs):
    if created:
        for tag in instance.movie.tags.all():
            update_tag_weight(instance.user, tag, delta=1.0)

@receiver(post_save, sender=RecommFeedback)
def update_preferences_from_feedback(sender, instance, created, **kwargs):
    if created:
        delta = 1.0 if instance.action_type in ['liked', 'smiled'] else -0.5
        for tag in instance.movie.tags.all():
            update_tag_weight(instance.user, tag, delta)
            
