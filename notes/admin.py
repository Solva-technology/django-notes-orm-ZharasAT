from django.contrib import admin

from notes.constants import SHORT_TEXT_MAX_LENGTH

from .models import Category, Note, Status, User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email")


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
    search_fields = ("text", "author__name")
    list_filter = ("status", "categories")

    @admin.display(description="Текст заметки")
    def short_text(self, obj):
        return obj.text[:SHORT_TEXT_MAX_LENGTH]

    @admin.display(description="Категории")
    def display_categories(self, obj):
        return ", ".join([cat.title for cat in obj.categories.all()])
