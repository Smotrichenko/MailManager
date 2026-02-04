from django.core.exceptions import PermissionDenied

from users.permissions import is_manager


class OwnerQuerySetMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        if is_manager(self.request.user):
            return qs
        return qs.filter(owner=self.request.user)


class ManagerReadOnlyForeignMixin:
    def dispatch(self, request, *args, **kwargs):
        if is_manager(request.user):
            obj = self.get_object()
            if obj.owner_id != request.user.id:
                raise PermissionDenied("Менеджер не может изменять чужие данные.")
        return super().dispatch(request, *args, **kwargs)
