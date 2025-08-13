from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import models

from notes.constants import NAME_MAX_LENGTH, NOTE_TEXT_PREVIEW_LENGTH


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", "id")


class User(AbstractUser):
    @property
    def name(self):
        return (self.get_full_name() or self.username).strip()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="profile",
    )
    bio = models.TextField(blank=True, verbose_name="Описание")
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата рождения"
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.name}"


class Status(BaseModel):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        blank=False,
        verbose_name="Имя"
    )
    is_final = models.BooleanField(verbose_name="Финальный статус")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Название"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"Категория {self.title}"


class Note(BaseModel):
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="notes"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name="Статус",
        related_name="notes"
    )
    categories = models.ManyToManyField(
        Category, verbose_name="Категории", related_name="notes"
    )

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        indexes = [
            GinIndex(
                SearchVector("text", config="russian"),
                name="note_text_fts_gin",
            ),
        ]

    def get_preview(self, length=NOTE_TEXT_PREVIEW_LENGTH):
        text = self.text or ""
        return text if len(text) <= length else f"{text[:length]}..."

    @property
    def preview(self):
        return self.get_preview()

    def __str__(self):
        return f"{self.preview} - {self.author.name}"
