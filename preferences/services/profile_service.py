from preferences.models import UserPreferenceProfile

def update_user_embedding(user, new_vector):
    profile, _ = UserPreferenceProfile.objects.get_or_create(user=user)
    profile.preference_embedding = new_vector
    profile.interaction_count += 1
    profile.save()
    return profile
