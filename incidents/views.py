from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import IncidentForm, IncidentUpdateForm
from .models import Incident, TimelineEvent


class IncidentListView(LoginRequiredMixin, ListView):
    model = Incident
    template_name = "incidents.html"
    context_object_name = "incidents"
    paginate_by = 10

    def get_queryset(self):
        queryset = Incident.objects.select_related("assigned_to", "created_by")

        # Search
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(incident_id__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
            )

        # Filters
        severity = self.request.GET.get("severity")
        if severity:
            queryset = queryset.filter(severity=severity)

        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)

        assigned_to = self.request.GET.get("assigned_to")
        if assigned_to:
            if assigned_to == "unassigned":
                queryset = queryset.filter(assigned_to__isnull=True)
            else:
                queryset = queryset.filter(assigned_to_id=assigned_to)

        # Sorting
        sort = self.request.GET.get("sort", "newest")
        if sort == "oldest":
            queryset = queryset.order_by("created_at")
        elif sort == "severity":
            # Note: naive alphabetical sort or we'd need Case/When for custom order, assuming naive is fine for now
            queryset = queryset.order_by("severity", "-created_at")
        elif sort == "status":
            queryset = queryset.order_by("status", "-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass filter choices to template
        from django.contrib.auth.models import User

        from .models import IncidentCategory, IncidentSeverity, IncidentStatus

        context["search_query"] = self.request.GET.get("q", "")
        context["severity_choices"] = IncidentSeverity.choices
        context["status_choices"] = IncidentStatus.choices
        context["category_choices"] = IncidentCategory.choices
        context["analysts"] = User.objects.filter(is_active=True).order_by("username")

        # Current active filters
        context["current_severity"] = self.request.GET.get("severity", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["current_category"] = self.request.GET.get("category", "")
        context["current_assigned_to"] = self.request.GET.get("assigned_to", "")
        context["current_sort"] = self.request.GET.get("sort", "newest")
        return context


class IncidentDetailView(LoginRequiredMixin, DetailView):
    model = Incident
    template_name = "incident_detail.html"
    context_object_name = "incident"
    slug_field = "incident_id"
    slug_url_kwarg = "incident_id"

    def get_queryset(self):
        return Incident.objects.select_related(
            "assigned_to", "created_by"
        ).prefetch_related("timeline_events", "attachments")


class IncidentCreateView(LoginRequiredMixin, CreateView):
    model = Incident
    form_class = IncidentForm
    template_name = "incident_form.html"
    context_object_name = "incident"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        incident = form.save()
        messages.success(
            self.request, f"Incident {incident.incident_id} created successfully."
        )
        return redirect("incidents")


class IncidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Incident
    form_class = IncidentUpdateForm
    template_name = "incident_form.html"
    context_object_name = "incident"
    slug_field = "incident_id"
    slug_url_kwarg = "incident_id"

    def form_valid(self, form):
        # Create a timeline event if status or assignee changed
        incident = form.save(commit=False)
        original = Incident.objects.get(pk=incident.pk)

        changes = []
        if original.status != incident.status:
            changes.append(
                f"Status changed from {original.status} to {incident.status}"
            )
        if original.assigned_to != incident.assigned_to:
            old_assignee = (
                original.assigned_to.username if original.assigned_to else "Unassigned"
            )
            new_assignee = (
                incident.assigned_to.username if incident.assigned_to else "Unassigned"
            )
            changes.append(f"Reassigned from {old_assignee} to {new_assignee}")

        incident.save()

        if changes:
            event_text = ", ".join(changes) + f" by {self.request.user.username}"
            TimelineEvent.objects.create(incident=incident, event=event_text)
            messages.success(
                self.request, f"Incident {incident.incident_id} updated successfully."
            )

        return redirect("incident_detail", incident_id=incident.incident_id)


class IncidentDeleteView(LoginRequiredMixin, DeleteView):
    model = Incident
    template_name = "incident_confirm_delete.html"
    slug_field = "incident_id"
    slug_url_kwarg = "incident_id"
    success_url = reverse_lazy("incidents")

    def delete(self, request, *args, **kwargs):
        incident = self.get_object()
        messages.success(
            request, f"Incident {incident.incident_id} was successfully deleted."
        )
        return super().delete(request, *args, **kwargs)
