import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Habit


@shared_task
def send_telegram_message(chat_id: int, text: str):
    """Отправляет сообщение в Telegram (с фолбэком в консоль при блокировке)."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        print(f"[TELEGRAM MOCK] Токен не задан. Сообщение для {chat_id}: {text}")
        return f'Sent to {chat_id} (mock)'

    url = f'https://api.telegram.org/bot{token}/sendMessage'

    try:
        # Пытаемся отправить реальное сообщение (с коротким таймаутом)
        response = requests.post(
            url,
            json={'chat_id': chat_id, 'text': text},
            timeout=3,
        )
        if response.status_code == 200:
            return f'Sent to {chat_id}'

        # Если Telegram вернул ошибку
        print(f"[TELEGRAM ERROR] {response.status_code}: {response.text}")
        return f'Error: {response.status_code}'

    except Exception as e:
        # Если сеть блокирует соединение, выводим в консоль (мок)
        print(f"[TELEGRAM MOCK] Сеть недоступна. Сообщение для {chat_id}: {text}")
        print(f"[TELEGRAM MOCK] Ошибка: {e}")
        return f'Sent to {chat_id} (mock)'


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о привычках (каждую минуту)."""
    now = timezone.now()
    habits = Habit.objects.filter(
        time__gte=(now - timedelta(minutes=1)).time(),
        time__lte=now.time(),
        owner__telegram_chat_id__isnull=False,
    )
    count = 0
    for habit in habits:
        text = f'Напоминание: {habit.action} в {habit.time.strftime("%H:%M")} в {habit.place}'
        send_telegram_message.delay(habit.owner.telegram_chat_id, text)
        count += 1
    return f'Sent {count} reminders'