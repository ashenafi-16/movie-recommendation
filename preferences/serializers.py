from rest_framework import serializers
from preferences.models import UserPreferenceProfile, UserTagPreference

class UserPreferenceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferenceProfile
        fields = '__all__'

class UserTagPreferenceSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = UserTagPreference
        fields = ["user_tag_pref_id", "user", "tag", "tag_name", "weight", "updated_at"]
 