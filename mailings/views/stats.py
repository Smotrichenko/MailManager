from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from mailings.models import Attempt
from users.permissions import is_manager


@method_decorator(cache_control(public=True, max_page=30), name="dispatch")
class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/stats.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        qs = Attempt.objects.select_related("mailing")
        if not is_manager(self.request.user):
            qs = qs.filter(mailing__owner=self.request.user)

        agg = qs.aggregate(
            success=Count("id", filter=Q(status=Attempt.STATUS_SUCCESS)),
            fail=Count("id", filter=Q(status=Attempt.STATUS_FAIL)),
        )

        ctx["success_attempts"] = agg["success"]
        ctx["fail_attempts"] = agg["fail"]
        ctx["sent_messages"] = agg["success"]

        return ctx
