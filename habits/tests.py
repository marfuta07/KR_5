from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='test12345')
        self.other = User.objects.create_user(email='other@test.com', password='test12345')
        self.client = APIClient()

        self.habit = Habit.objects.create(
            owner=self.user,
            place='Дом',
            time='08:00:00',
            action='Выпить воду',
            duration=60,
            periodicity=1,
            is_public=False,
        )

    def test_create_habit(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'place': 'Спортзал',
            'time': '18:00:00',
            'action': 'Сделать зарядку',
            'duration': 30,
            'periodicity': 1,
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_list_habits(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_habit(self):
        self.client.force_authenticate(user=self.user)
        data = {'action': 'Выпить 2 стакана воды'}
        response = self.client.patch(f'/api/habits/{self.habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Выпить 2 стакана воды')

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_user_cannot_access_other_habit(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ValidatorsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='test12345')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_duration_exceeds_120(self):
        data = {'place': 'Дом', 'time': '08:00:00', 'action': 'Тест', 'duration': 200, 'periodicity': 1}
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('duration', response.data)

    def test_periodicity_exceeds_7(self):
        data = {'place': 'Дом', 'time': '08:00:00', 'action': 'Тест', 'duration': 60, 'periodicity': 10}
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('periodicity', response.data)

    def test_pleasant_habit_cannot_have_reward(self):
        data = {
            'place': 'Дом', 'time': '08:00:00', 'action': 'Тест',
            'duration': 60, 'periodicity': 1,
            'is_pleasant': True, 'reward': 'Конфета'
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PublicHabitsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='test12345')
        self.other = User.objects.create_user(email='other@test.com', password='test12345')
        self.client = APIClient()

        self.public_habit = Habit.objects.create(
            owner=self.user, place='Дом', time='08:00:00', action='Публичная',
            duration=60, periodicity=1, is_public=True,
        )

    def test_other_user_sees_public_habit(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
