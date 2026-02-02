from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mailings.models import Attempt, Mailings


class Command(BaseCommand):
    """Ручной запуск рассылки через команду"""

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        mailing = Mailings.objects.get(pk=mailing_id)
        mailing.update_status()

        now = timezone.now()

        if not (mailing.start_time) <= now <= (mailing.end_time):
            self.stdout.write(
                self.style.ERROR("Отправка запрещена: время вне интервала")
            )
            return

        recipients = mailing.recipients.all()
        if not recipients.exists():
            self.stdout.write(self.style.ERROR("У рассылки нет получателей"))
            return

        for r in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,
                    recipient_list=[r.email],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    mailing=mailing,
                    status=Attempt.STATUS_SUCCESS,
                    server_response="OK",
                )
            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    status=Attempt.STATUS_FAIL,
                    server_response=str(e),
                )
        self.stdout.write(self.style.SUCCESS("Готово!Рассылка отправлена."))
