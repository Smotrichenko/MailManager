from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from mailings.forms import RecipientForm
from mailings.mixins import ManagerReadOnlyForeignMixin, OwnerQuerySetMixin
from mailings.models import Recipient


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
