from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Recipient(models.Model):
    """ Модель 'Получатель рассылки' """

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} {self.email}"


class Message(models.Model):
    """ Модель 'Сообщение' """

    subject = models.CharField(max_length=300, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject


class Mailings(models.Model):
    """ Модель 'Рассылка' """

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Запущена"
    STATUS_FINISHED = "Завершена"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        Message, on_delete=CASCADE, related_name="mailings", verbose_name="Сообщение"
    )
    recipients = models.ManyToManyField(
        Recipient, related_name="mailings", verbose_name="Получатели"
    )

    def __str__(self):
        return f"Рассылка №{self.pk} ({self.status})"

    def clean(self):
        now = timezone.now()

        if self.start_time and self.start_time < now:
            raise ValidationError({"start_time": "start_time не может быть в прошлом."})

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                {"end_time": "end_time должен быть позже start_time."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_STARTED
        else:
            new_status = self.STATUS_FINISHED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class Attempt(models.Model):
    """ Модель 'Попытка рассылки' """

    STATUS_SUCCESS = "Успешно"
    STATUS_FAIL = "Не успешно"

    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAIL, "Не успешно"),
    ]

    attempt_time = models.DateTimeField(
        default=timezone.now, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True, verbose_name="Ответ почтового сервера"
    )
    mailing = models.ForeignKey(
        Mailings, on_delete=CASCADE, related_name="attempts", verbose_name="Рассылка"
    )

    def __str__(self):
        return f"Attempt №{self.pk}: {self.mailing_id} ({self.status})"
