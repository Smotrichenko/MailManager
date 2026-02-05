from smtplib import SMTPException

from django.core.mail import send_mail
from django.utils import timezone

from mailings.exceptions import (
    InvalidMailingIntervalError,
    MailingDisabledError,
    NoRecipientsError,
)
from mailings.models import Attempt, Mailings


def send_mailing(mailing_id: int) -> None:
    mailing = (
        Mailings.objects.select_related("message")
        .prefetch_related("recipients")
        .get(pk=mailing_id)
    )

    if not mailing.is_enabled:
        raise MailingDisabledError

    mailing.update_status()
    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        raise InvalidMailingIntervalError

    recipients = mailing.recipients.all()
    if not recipients.exists():
        raise NoRecipientsError

    attempts = []
    for recipient in recipients:
        attempt = Attempt(mailing=mailing)
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
        except SMTPException as e:
            attempt.status = Attempt.STATUS_FAIL
            attempt.server_response = str(e)
        else:
            attempt.status = Attempt.STATUS_SUCCESS
            attempt.server_response = None
        attempts.append(attempt)

    if attempts:
        Attempt.object.bulk_create(attempts)
