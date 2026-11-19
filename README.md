# Курсовая работа "Habit Tracker API"

Бэкенд-часть SPA веб-приложения для трекера 
полезных привычек.
## Описание задач
- Добавьте необходимые модели привычек.
- Реализуйте эндпоинты для работы с фронтендом.
- Создайте приложение для работы с Telegram и рассылками напоминани
## Стек

- Python 3.14, Django 6.1, Django REST Framework
- JWT-аутентификация (`djangorestframework-simplejwt`)
- Celery + Redis (фоновые задачи)
- drf-spectacular (Swagger)
- CORS (`django-cors-headers`)

## Установка

```bash
git clone https://github.com/marfuta07/KR_5.git
cd KR_5
poetry install
