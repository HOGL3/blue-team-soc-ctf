from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("release-notes/", views.release_notes_view, name="release_notes"),
    path("help/", views.help_view, name="help"),
]
