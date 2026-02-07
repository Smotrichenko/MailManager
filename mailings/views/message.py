from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from mailings.forms import MessageForm
from mailings.mixins import ManagerReadOnlyForeignMixin, OwnerQuerySetMixin
from mailings.models import Message


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
