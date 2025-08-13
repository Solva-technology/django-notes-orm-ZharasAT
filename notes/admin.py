from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from notes.constants import NOTE_TEXT_PREVIEW_LENGTH

from .models import Category, Note, Status, UserProfile

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", "username",
        "name",
        "email",
        "date_joined",
        "is_staff"
    )
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "birth_date")
    search_fields = ("user__name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_final")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    search_fields = ("title",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_text",
        "author",
        "status",
        "display_categories",
        "created_at",
    )
    search_fields = ("@text", "^author__name")
    search_help_text = "Искать по началу имени автора и по тексту заметки."
    list_filter = ("status", "categories")

    def get_queryset(self, request):
        return (super().get_queryset(request)
                .select_related("author", "status")
                .prefetch_related("categories"))

    @admin.display(description="Текст заметки")
    def short_text(self, obj):
        return obj.get_preview(NOTE_TEXT_PREVIEW_LENGTH)

    @admin.display(description="Категории")
    def display_categories(self, obj):
        return ", ".join([cat.title for cat in obj.categories.all()])
