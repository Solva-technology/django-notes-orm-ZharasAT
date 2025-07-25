# Мини-сервис заметок

Django-приложение для хранения и просмотра пользовательских заметок. Реализовано с использованием PostgreSQL и Docker, поддерживает полноценную работу с моделями через Django ORM и отображение данных через шаблоны.

## Стек технологий
- Python
- Django
- PostgreSQL
- Docker, Docker Compose
- Bootstrap
- dotenv

## Запуск проекта
1. Клонируйте репозиторий и перейдите в каталог проекта:

  `git clone git@github.com:Solva-technology/django-notes-orm-ZharasAT.git`

  `cd django-notes-orm-ZharasAT`

2. Создайте .env на основе .env.example файла в корне проекта.

3. Соберите и запустите контейнеры:

  `docker-compose up --build`

4. Создайте и примените миграции:

  `docker-compose exec web python manage.py makemigrations`

  `docker-compose exec web python manage.py migrate`

5. Загрузите тестовые данные:

  `docker-compose exec web python manage.py loaddata notes/fixtures/initial_data.json`

Откройте в браузере: http://localhost:8000

6. Создайте суперпользователя (по желанию):

  `docker-compose exec web python manage.py createsuperuser`

Админка доступна по адресу: http://localhost:8000/admin

## Основной функционал

### Главная страница — список заметок

* URL: /

- Отображает все заметки с:
  - обрезанным текстом (до 100 символов),
  - именем автора,
  - статусом,
  - списком категорий,
  - датой создания.

Оптимизация ORM: `select_related("author", "status")`, `prefetch_related("categories")`

### Страница заметки

* URL: /notes/<int:note_id>/

- Полный текст заметки
- Имя, email, биография, дата рождения автора
- Статус (с отметкой, является ли он финальным)
- Список категорий

Используется `select_related("author", "author__profile", "status")`, `prefetch_related("categories")`

### Страница пользователя
* URL: /users/<int:user_id>/

- Имя пользователя, email, биография, дата рождения

- Список всех заметок пользователя с указанием текста и статуса

Используется `select_related("profile")`, `prefetch_related("notes__status")`

## Структура проекта

notebook_project/
├── notes/
│   ├── models.py        # User, Note, Status, Category, UserProfile
│   ├── views.py         # Представления для отображения данных
│   ├── templates/       # Шаблоны: базовый и три пользовательских
│   ├── fixtures/        # Фикстуры для тестовых данных
│   └── admin.py         # Кастомизация админки
├── notebook_project/
│   └── settings.py      # Настройки Django + .env подключение
├── docker-compose.yml   # Контейнеры web и db
├── Dockerfile           # Django-образ
├── .env.example         # Шаблон переменных окружения
└── README.md            # Описание проекта

## Тестовые данные
В проекте используется файл initial_data.json — он содержит готового пользователя, профиль, статусы, категории и заметки.

## Автор - https://github.com/ZharasAT