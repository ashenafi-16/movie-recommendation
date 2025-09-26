import logging
from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Profile
from .base.store_token import set_token_cookies
from .tasks import fetch_and_save_avatar
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def link_to_existing_user_by_email(strategy, details, backend, uid=None, user=None, *args, **kwargs):

    if user:
        return {"user": user}

    email = details.get("email") or (kwargs.get("response") or {}).get("email")
    if not email:
        return

    existing = CustomUser.objects.filter(email__iexact=email).first()
    if not existing:
        return

    if not UserSocialAuth.objects.filter(user=existing, provider=backend.name).exists():
        if uid is None:
            uid = strategy.storage.user.get_social_auth_uid(backend, kwargs.get("response") or {})
        try:
            UserSocialAuth.objects.create(user=existing, uid=uid, provider=backend.name)
        except Exception as e:
            logger.warning("Race condition when linking social account: %s", e)

    return {"user": existing}


def save_oauth_provider_and_name(strategy, details, backend, user=None, response=None, is_new=False, *args, **kwargs):
    """
    Save provider (google/facebook), update name, and activate user if needed.
    """
    if not user:
        return

    changed = False

    provider_name = backend.name
    if user.oauth_provider != provider_name:
        user.oauth_provider = provider_name
        changed = True

    # Update display name
    name = (details or {}).get("fullname") or (response or {}).get("name") or (details or {}).get("username")
    if not name:
        user.name = name
        changed = True

    # Auto-activate if inactive
    if not user.is_active:
        user.is_active = True
        changed = True

    if changed:
        user.save(update_fields=["oauth_provider", "name", "is_active"])

    return {"user": user}



def store_jwt_tokens_in_session(strategy, details, backend, user=None, *args, **kwargs):
    if user is None:
        return

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = redirect('/')

    set_token_cookies(response, access_token, refresh_token)

    return response



def enqueue_avatar_task(strategy, backend, user=None, response=None, *args, **kwargs):
    if not user:
        return

    profile, _ = Profile.objects.get_or_create(user=user)

    if profile.avatar:
        logger.debug("User %s already has avatar, skip enqueue.", user.id)
        return

    avatar_url = None
    if backend.name == "google-oauth2":
        avatar_url = response.get("picture") if response else None
    elif backend.name == "facebook":
        if response:
            pic = response.get("picture")
            if isinstance(pic, dict):
                avatar_url = pic.get("data", {}).get("url")
            elif response.get("id"):
                avatar_url = f"https://graph.facebook.com/{response['id']}/picture?type=large"

    if avatar_url:
        fetch_and_save_avatar.delay(user.id, avatar_url)
        logger.info("Enqueued avatar fetch task for user=%s", user.id)
