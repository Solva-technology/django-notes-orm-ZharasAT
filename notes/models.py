from django.db import models

from notes.constants import CHARFIELD_MAX, NOTE_TEXT_PREVIEW_LENGTH


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=CHARFIELD_MAX, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    user = models.OneToOneField(
        User,
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
    name = models.CharField(max_length=CHARFIELD_MAX, verbose_name="Имя")
    is_final = models.BooleanField(
        null=False,
        blank=False,
        verbose_name="Заполнена"
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField(
        max_length=CHARFIELD_MAX,
        verbose_name="Название"
    )
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"Категория {self.title}"


class Note(BaseModel):
    text = models.TextField(blank=False, verbose_name="Текст")
    author = models.ForeignKey(
        User,
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

    def __str__(self):
        preview = self.text[:NOTE_TEXT_PREVIEW_LENGTH]
        return f"{preview}... - {self.author.name}"
