from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View

from .forms import UserProfileUpdateForm, UserUpdateForm
from .models import Notification, UserProfile


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        # Removed vulnerable login logic
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    """
    Read-only view for the authenticated user's profile.
    Prevents IDOR by strictly binding to request.user.
    """
    try:
        profile = UserProfile.objects.select_related("user").get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, "profile.html", {"profile": profile})


@login_required
def profile_update_view(request):
    """
    Allows users to update their own profile fields.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            # If profile didn't exist, we need to create it and bind to user
            profile_instance = p_form.save(commit=False)
            profile_instance.user = request.user
            profile_instance.save()

            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "profile_form.html", context)


# --- Notification Centre ---


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self):
        # Strict filter preventing IDOR
        return Notification.objects.filter(user=self.request.user)


class NotificationUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, action):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        if action == "read":
            notification.is_read = True
            messages.success(request, "Notification marked as read.")
        elif action == "unread":
            notification.is_read = False
            messages.success(request, "Notification marked as unread.")
        notification.save()
        return redirect("notifications")


class NotificationMarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        messages.success(request, "All notifications marked as read.")
        return redirect("notifications")
