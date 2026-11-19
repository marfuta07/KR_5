from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """Модель привычки."""

    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Каждые 2 дня'),
        (3, 'Каждые 3 дня'),
        (7, 'Еженедельно'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь',
    )
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=200, verbose_name='Действие')
    is_pleasant = models.BooleanField(
        default=False, verbose_name='Приятная привычка'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='related_habits',
        verbose_name='Связанная привычка',
    )
    periodicity = models.PositiveIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name='Периодичность (дни)',
    )
    reward = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Вознаграждение'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Время на выполнение (сек)'
    )
    is_public = models.BooleanField(
        default=False, verbose_name='Публичная'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.owner.email} — {self.action}'

    def clean(self):
        """Валидация модели."""
        if self.related_habit and self.reward:
            raise ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )
        if self.duration and self.duration > 120:
            raise ValidationError(
                'Время выполнения не должно превышать 120 секунд.'
            )
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                'Связанная привычка должна быть приятной.'
            )
        if self.is_pleasant:
            if self.reward:
                raise ValidationError(
                    'У приятной привычки не может быть вознаграждения.'
                )
            if self.related_habit:
                raise ValidationError(
                    'У приятной привычки не может быть связанной привычки.'
                )
        if self.periodicity and self.periodicity > 7:
            raise ValidationError(
                'Периодичность не может быть больше 7 дней.'
            )
