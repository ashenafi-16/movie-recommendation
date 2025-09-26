from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def email_verification_message(user_email):
    subject = 'welcome to movie recommendation 🎬'
    message = "Thank you for registering! please verify your account."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
    
    return f"Email sent to {user_email}"
@shared_task
def password_reset(reset_link, user_email):
    subject = 'password rest'
    message = f"Reset your password \n Click here to reset your password: {reset_link}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject,message,from_email,recipient_list)


import logging
import requests
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Profile

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def fetch_and_save_avatar(self, user_id, avatar_url):
    try:
        user = User.objects.get(pk=user_id)
        profile, _ = Profile.objects.get_or_create(user=user)

        if profile.avatar:
            logger.debug("User %s already has avatar; skipping.", user_id)
            return

        resp = requests.get(avatar_url, timeout=8)
        resp.raise_for_status()

        if len(resp.content) > 5 * 1024 * 1024:
            logger.warning("Avatar too large for user=%s (size=%s)", user_id, len(resp.content))
            return

        content_type = resp.headers.get("Content-Type", "").lower()
        ext = "jpg"
        if content_type.startswith("image/"):
            ext = content_type.split("/")[-1].split(";")[0] or "jpg"

        filename = f"user_{user.id}_avatar.{ext}"

        with transaction.atomic():
            profile.avatar.save(filename, ContentFile(resp.content), save=True)

        logger.info("Avatar saved for user=%s", user.id)

    except User.DoesNotExist:
        logger.warning("User %s not found for avatar fetch", user_id)
        return
    except Exception as exc:
        logger.exception("Failed to save avatar for user=%s: %s", user_id, exc)
        raise self.retry(exc=exc)