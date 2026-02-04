from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import ListView, View

from .models import User
from .permissions import is_manager


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/user_list.html"

    def dispatch(self, request, *args, **kwargs):
        if not is_manager(request.user):
            raise PermissionDenied("Доступ только для менеджера.")
        return super().dispatch(request, *args, **kwargs)


class ToggleUserBlockView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not is_manager(request.user):
            raise PermissionDenied("Доступ только для менеджера.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])
        return redirect("user_list")
