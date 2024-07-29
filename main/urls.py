from django.urls import path

from .views import EventsListView

app_name = "main"

urlpatterns = [
    path("events-list/", EventsListView.as_view(), name="events-list"),
]
