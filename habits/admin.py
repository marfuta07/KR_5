from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'time', 'periodicity', 'is_public')
    list_filter = ('is_public', 'periodicity')
    search_fields = ('action', 'owner__email')
