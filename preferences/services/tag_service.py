from preferences.models import UserTagPreference

def update_tag_weight(user, tag, delta=1.0):

    tag_pref, _ = UserTagPreference.objects.get_or_create(user=user, tag=tag)
    tag_pref.weight += delta
    tag_pref.save()
    return tag_pref