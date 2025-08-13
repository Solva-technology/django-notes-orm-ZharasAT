from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.notes_home, name="notes_home"),
    path("notes/<int:note_id>/", views.note_detail, name="note_detail"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
]
