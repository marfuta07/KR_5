# Курсовая работа №6
# Habit Tracker API

Бэкенд-часть SPA веб-приложения для трекера полезных привычек.

## Описание задач
- Реализованы модели привычек с валидацией.
- Настроены эндпоинты для работы с фронтендом.
- Интегрирован Telegram-бот для рассылки напоминаний через Celery.
- Настроена пагинация, права доступа и CORS.
- Добавлена документация через Swagger (drf-spectacular).

## Стек

- Python 3.12 (в Docker), Django 6.1, Django REST Framework
- JWT-аутентификация (`djangorestframework-simplejwt`)
- Celery + Redis (фоновые задачи и напоминания)
- drf-spectacular (Swagger)
- CORS (`django-cors-headers`)
- Docker, Docker Compose, Nginx
- CI/CD через GitHub Actions

---

## 🚀 Запуск проекта локально (без Docker)

### 1. Клонирование и установка
```bash
git clone https://github.com/marfuta07/KR_5.git
cd KR_5
poetry install


3. Миграции и запуск
bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
Запуск Celery (в отдельных терминалах):

bash
poetry run celery -A config worker -l info -P solo
poetry run celery -A config beat -l info
🐳 Запуск через Docker (Production)
Проект полностью контейнеризирован. 
Для запуска на сервере или локально используйте 
docker-compose.prod.yml.

1. Подготовка
Убедитесь, что на сервере установлены Docker и Docker Compose.
Создайте файл .env на сервере с теми же переменными, что и выше (обязательно укажите DB_HOST=db и REDIS_URL=redis://redis:6379/0).

2. Запуск контейнеров
bash
docker compose -f docker-compose.prod.yml up -d --build
3. Сбор статики
bash
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
4. Доступ к приложению
Swagger API: http://<IP_сервера>/api/docs/

Админка Django: http://<IP_сервера>/admin/

🔄 CI/CD и Деплой (GitHub Actions)
В проекте настроен пайплайн GitHub Actions (.github/workflows/deploy.yml), который при пуше в ветку main:

Запускает тесты и линтер (flake8).

Собирает Docker-образ и пушит его в GitHub Container Registry (GHCR).

Автоматически деплоит проект на удаленный сервер по SSH.

Необходимые секреты в GitHub (Settings -> Secrets -> Actions):
SSH_HOST — IP-адрес сервера.

SSH_USER — имя пользователя (например, root).

SSH_PRIVATE_KEY — приватный SSH-ключ для доступа к серверу.

🔗 Ссылки
Репозиторий: https://github.com/marfuta07/KR_5

Работающий сервер (Swagger): http://147.45.154.102/api/docs/

Автор: Юлия Бусыгина