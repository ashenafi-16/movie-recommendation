import uuid
from django.db import models
from django.conf import settings
from movies.models import MovieDetail

class Recommendation(models.Model):
    recom_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommendations")
    movie = models.ForeignKey(MovieDetail, on_delete=models.CASCADE, related_name="recommendation_to")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation: {self.user.email} --> {self.movie.title}"
    
class RecommFeedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommend_feedbacks")
    movie = models.ForeignKey(MovieDetail, on_delete=models.CASCADE, related_name='feedbacks')
    action_type = models.CharField(max_length=50, choices=[
        ("liked", 'Liked'),
        ('disliked', 'Disliked'),
        ('skipped', 'Skipped'),
        ('clicked', 'Clicked'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.action_type} {self.movie.title}"
    