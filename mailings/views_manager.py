from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views import View

from users.permissions import is_manager

from .models import Mailings


class ToggleMailingEnabledView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not is_manager(request.user):
            raise PermissionDenied("Доступ только для менеджера.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        mailing = Mailings.objects.get(pk=pk)
        mailing.is_enabled = not mailing.is_enabled
        mailing.save(update_fields=["is_enabled"])
        return redirect("mailing_detail", pk=pk)
