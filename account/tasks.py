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