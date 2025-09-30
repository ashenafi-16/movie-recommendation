from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RecommFeedback
from preferences.services.tag_service import update_tag_weight

@receiver(post_save, sender=RecommFeedback)
def update_preferences_from_feedback(sender, instance, created, **kwargs):
    if created:
        delta = 1.0 if instance.action_type == "liked" else -0.5
        for tag in instance.movie.tags.all():
            update_tag_weight(instance.user, tag, delta)