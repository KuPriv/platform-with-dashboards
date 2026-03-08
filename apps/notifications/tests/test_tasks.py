from unittest.mock import patch

import pytest
from django.conf import settings

from apps.notifications.tasks import send_email


@pytest.mark.django_db
def test_get_nonexist_user_returns_does_not_exist():
    with patch("apps.notifications.tasks.send_mail") as mock_mail:
        assert send_email(1, "subject_test", "message_test") is None
    assert mock_mail.call_count == 0


@pytest.mark.django_db
def test_send_mail_is_successful(user):
    with patch("apps.notifications.tasks.send_mail") as mock_mail:
        send_email(user.pk, "subject_test", "message_test")
        mock_mail.assert_called_once_with(
            subject="subject_test",
            message="message_test",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
