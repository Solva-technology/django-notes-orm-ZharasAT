from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from .models import Note

User = get_user_model()


def notes_home(request):
    notes = (
        Note.objects.select_related("author", "status")
        .prefetch_related("categories")
        .order_by("-created_at")
    )
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, note_id):
    note = get_object_or_404(
        Note.objects
            .select_related("author", "author__profile", "status")
            .prefetch_related("categories"),
        pk=note_id,
    )
    return render(request, "notes/note_detail.html", {"note": note})


def user_detail(request, user_id):
    user = get_object_or_404(
        User.objects
            .select_related("profile")
            .prefetch_related("notes__status"),
        pk=user_id,
    )
    return render(request, "notes/user_detail.html", {"user": user})
