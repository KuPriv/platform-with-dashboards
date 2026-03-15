import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task(ignore_result=True)
def send_email(user_pk, subject, message):
    try:
        user = User.objects.get(pk=user_pk)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        logger.info("Email sent to %s", user.email)
    except User.DoesNotExist:
        logger.error("User %s not found", user_pk)
        return
