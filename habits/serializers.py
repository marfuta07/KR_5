from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('owner',)

    def validate_duration(self, value):
        if value > 120:
            raise serializers.ValidationError('Время выполнения не должно превышать 120 секунд.')
        return value

    def validate_periodicity(self, value):
        if value > 7:
            raise serializers.ValidationError('Периодичность не может быть больше 7 дней.')
        return value

    def validate(self, data):
        # 1. Одновременный выбор связанной привычки и вознаграждения
        if data.get('related_habit') and data.get('reward'):
            raise serializers.ValidationError(
                'Нельзя одновременно указать связанную привычку и вознаграждение.'
            )

        # 2. Связанная привычка должна быть приятной
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной.'
            )

        # 3. У приятной привычки не может быть вознаграждения или связанной привычки
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть вознаграждения.'
                )
            if data.get('related_habit'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки.'
                )

        return data