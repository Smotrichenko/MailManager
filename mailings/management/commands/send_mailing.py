from django.core.management.base import BaseCommand

from mailings.exceptions import (
    InvalidMailingIntervalError,
    MailingDisabledError,
    NoRecipientsError,
)
from mailings.use_cases import send_mailing


class Command(BaseCommand):
    """Ручной запуск рассылки через команду"""

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        try:
            send_mailing(mailing_id=mailing_id)
        except MailingDisabledError:
            self.stdout.write(self.style.ERROR("Рассылка отключена менеджером."))
        except InvalidMailingIntervalError:
            self.stdout.write(
                self.style.ERROR("Отправка запрещена: время вне интервала.")
            )
        except NoRecipientsError:
            self.stdout.write(self.style.ERROR("У рассылки нет получателей."))
        else:
            self.stdout.write(self.style.SUCCESS("Рассылка отправлена."))
