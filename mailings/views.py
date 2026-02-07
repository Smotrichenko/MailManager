from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from mailings.exceptions import (
    InvalidMailingIntervalError,
    MailingDisabledError,
    NoRecipientsError,
)
from mailings.forms import MailingsForm, MessageForm, RecipientForm
from mailings.mixins import ManagerReadOnlyForeignMixin, OwnerQuerySetMixin
from mailings.models import Mailings, Message, Recipient
from mailings.use_cases import send_mailing


class HomeView(TemplateView):
    """Главная страница со статистикой"""

    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        Mailings.objects.update_status()

        for mailing in Mailings.objects.all():
            mailing.update_status()

        now = timezone.now()

        context["total_mailings"] = Mailings.objects.count()

        context["active_mailings"] = Mailings.objects.filter(
            start_time__lte=now, end_time__gte=now, status=Mailings.STATUS_STARTED
        ).count()

        context["unique_recipients"] = Recipient.objects.count()

        return context


class RecipientListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(
    LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, UpdateView
):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientDeleteView(
    LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, DeleteView
):
    model = Recipient
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")


class MessageListView(LoginRequiredMixin, OwnerQuerySetMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, DeleteView):
    model = Message
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


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


class MailingsCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    form_class = MailingsForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingsUpdateView(
    LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, UpdateView
):
    model = Mailings
    form_class = MailingsForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingsDeleteView(
    LoginRequiredMixin, OwnerQuerySetMixin, ManagerReadOnlyForeignMixin, DeleteView
):
    model = Mailings
    template_name = "mailings/confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


def send_mailing_view(request, pk: int):
    """Ручной запуск рассылки через интерфейс"""

    mailing = get_object_or_404(Mailings, pk=pk)

    try:
        send_mailing(mailing_id=mailing.pk)
    except MailingDisabledError:
        messages.error(request, "Рассылка отключена менеджером.")
    except InvalidMailingIntervalError:
        messages.error(
            request, "Отправка запрещена: текущее время не входит в интервал рассылки."
        )
    except NoRecipientsError:
        messages.error(request, "У рассылки нет получателей.")
    else:
        messages.success(request, "Рассылка отправлена.")

    return redirect("mailing_detail", pk=pk)
