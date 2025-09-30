import uuid
from django.db import models
from django.conf import settings

class UserPreferenceProfile(models.Model):
    preference_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference_profile")
    preference_embedding = models.JSONField(null=True, blank=True, )
    interaction_count = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Preference of {self.user.email}"
    
    
class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class UserTagPreference(models.Model):
    user_tag_pref_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tag_preferences")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="user_preferences")
    weight = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tag')
    
    def __str__(self):
        return f"{self.user.email} -> {self.tag.name}({self.weight})"
    