from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from mailings.forms import MailingsForm, MessageForm, RecipientForm
from mailings.models import Attempt, Mailings, Message, Recipient


class HomeView(TemplateView):
    """Главная страница со статистикой"""

    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for mailing in Mailings.objects.all():
            mailing.update_status()

        now = timezone.now

        context["total_mailings"] = Mailings.objects.count()

        context["active_mailings"] = Mailings.objects.filter(
            start_time_lte=now, end_time_dte=now, status=Mailings.STATUS_STARTED
        ).count()

        context["unique_repicients"] = Recipient.object.count()

        return context


class RecipientListView(ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("recipient_list")


class MessageListView(ListView):
    model = Message
    template_name = "mailings/message_list.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("message_list")


class MailingsListView(ListView):
    model = Mailings
    template_name = "mailings/mailing_list.html"


class MailingsDetailView(DeleteView):
    model = Mailings
    template_name = "mailings/mailing_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailingsCreateView(CreateView):
    model = Mailings
    form_class = MailingsForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailing_list")


class MailingsUpdateView(UpdateView):
    model = Mailings
    form_class = MailingsForm
    template_name = "mailings/form.html"
    success_url = reverse_lazy("mailing_list")


class MailingsDeleteView(DeleteView):
    model = Mailings
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailing_list")


def send_mailing_view(request, pk: int):
    """Ручной запуск рассылки через интерфейс"""

    mailing = Mailings.objects.get(pk=pk)
    mailing.update_status()

    now = timezone.now()

    if not (mailing.start_time <= now <= mailing.end_time):
        messages.error(
            request, "Отправка запрещена: текущее время не входит в интервал рассылки"
        )
    return redirect("mailing_detail", pk=pk)

    recipients = mailing.recipients.all()
    if not recipients.exists():
        messages.error(requests, "У рассылки нет получателей")
    return redirect("mailing_detail", pk=pk)

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

    messages.success(request, "Рассылка отправлена")
    return redirect("mailing_detail", pk=pk)
