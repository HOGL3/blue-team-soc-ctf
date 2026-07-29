from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from .models import ActivityLog, ActivityType


class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = "activity_logs.html"
    context_object_name = "activities"
    paginate_by = 15

    def get_queryset(self):
        # We want to show all activity logs but optimize queries.
        qs = ActivityLog.objects.select_related("performed_by").all()

        # Filtering logic
        q_search = self.request.GET.get("q")
        user_search = self.request.GET.get("user")
        action_type = self.request.GET.get("action_type")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        if q_search:
            qs = qs.filter(
                Q(target_object__icontains=q_search)
                | Q(description__icontains=q_search)
            )

        if user_search:
            qs = qs.filter(performed_by__username__icontains=user_search)

        if action_type:
            qs = qs.filter(action_type=action_type)

        if date_from:
            qs = qs.filter(timestamp__date__gte=date_from)

        if date_to:
            qs = qs.filter(timestamp__date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_types"] = ActivityType.choices
        # Keep track of current filters to prepopulate the form
        context["current_filters"] = {
            "q": self.request.GET.get("q", ""),
            "user": self.request.GET.get("user", ""),
            "action_type": self.request.GET.get("action_type", ""),
            "date_from": self.request.GET.get("date_from", ""),
            "date_to": self.request.GET.get("date_to", ""),
        }
        return context
