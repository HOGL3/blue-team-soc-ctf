from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import AssetForm
from .models import Asset, AssetCriticality, AssetStatus, AssetType


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets.html"
    context_object_name = "assets"
    paginate_by = 10

    def get_queryset(self):
        queryset = Asset.objects.select_related("owner")

        # Search: Asset Name, Hostname, IP Address, Operating System, Owner
        search_query = self.request.GET.get("q", "").strip()
        if search_query:
            queryset = queryset.filter(
                Q(asset_name__icontains=search_query)
                | Q(hostname__icontains=search_query)
                | Q(ip_address__icontains=search_query)
                | Q(operating_system__icontains=search_query)
                | Q(owner__username__icontains=search_query)
            )

        # Filters: Asset Type, Criticality, Status, Owner, Operating System
        asset_type = self.request.GET.get("asset_type")
        if asset_type:
            queryset = queryset.filter(asset_type=asset_type)

        criticality = self.request.GET.get("criticality")
        if criticality:
            queryset = queryset.filter(criticality=criticality)

        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        operating_system = self.request.GET.get("operating_system")
        if operating_system:
            queryset = queryset.filter(operating_system=operating_system)

        owner = self.request.GET.get("owner")
        if owner:
            if owner == "unassigned":
                queryset = queryset.filter(owner__isnull=True)
            else:
                queryset = queryset.filter(owner_id=owner)

        # Sorting
        sort = self.request.GET.get("sort", "newest")
        if sort == "oldest":
            queryset = queryset.order_by("created_at")
        elif sort == "name":
            queryset = queryset.order_by("asset_name")
        elif sort == "criticality":
            queryset = queryset.order_by("criticality", "-created_at")
        elif sort == "status":
            queryset = queryset.order_by("status", "-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User

        # Pass choices for filters
        context["search_query"] = self.request.GET.get("q", "")
        context["type_choices"] = AssetType.choices
        context["criticality_choices"] = AssetCriticality.choices
        context["status_choices"] = AssetStatus.choices
        context["owners"] = User.objects.filter(is_active=True).order_by("username")

        # Distinct OS choices
        os_list = (
            Asset.objects.exclude(operating_system__isnull=True)
            .exclude(operating_system__exact="")
            .values_list("operating_system", flat=True)
            .distinct()
            .order_by("operating_system")
        )
        context["os_choices"] = os_list

        # Current active filters
        context["current_type"] = self.request.GET.get("asset_type", "")
        context["current_criticality"] = self.request.GET.get("criticality", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["current_os"] = self.request.GET.get("operating_system", "")
        context["current_owner"] = self.request.GET.get("owner", "")
        context["current_sort"] = self.request.GET.get("sort", "newest")

        return context


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    template_name = "asset_detail.html"
    context_object_name = "asset"

    def get_queryset(self):
        return Asset.objects.select_related("owner")


class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset_form.html"

    def form_valid(self, form):
        messages.success(
            self.request, f"Asset '{form.instance.asset_name}' created successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("asset_detail", kwargs={"pk": self.object.pk})


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "asset_form.html"

    def form_valid(self, form):
        messages.success(
            self.request, f"Asset '{form.instance.asset_name}' updated successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("asset_detail", kwargs={"pk": self.object.pk})


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    template_name = "asset_confirm_delete.html"
    success_url = reverse_lazy("assets")

    def delete(self, request, *args, **kwargs):
        asset = self.get_object()
        messages.success(
            request, f"Asset '{asset.asset_name}' was successfully deleted."
        )
        return super().delete(request, *args, **kwargs)
