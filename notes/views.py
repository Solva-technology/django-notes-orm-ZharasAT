from django.shortcuts import render

from .models import Note, User


def notes_home(request):
    notes = (
        Note.objects.select_related("author", "status")
        .prefetch_related("categories")
        .order_by("-created_at")
    )
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, note_id):
    note = (
        Note.objects.select_related("author", "author__profile", "status")
        .prefetch_related("categories")
        .get(pk=note_id)
    )
    return render(request, "notes/note_detail.html", {"note": note})


def user_detail(request, user_id):
    user = (
        User.objects.select_related("profile")
        .prefetch_related("notes__status")
        .get(pk=user_id)
    )
    return render(request, "notes/user_detail.html", {"user": user})
