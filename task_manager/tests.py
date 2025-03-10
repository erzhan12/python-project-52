# from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from task_manager.models import Status


class UserCRUDTestCase(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def setUp(self):
        self.client = Client()
        # Создаём пользователей напрямую вместо использования фикстур
        self.user1 = User.objects.get(username='testuser1')
        self.user2 = User.objects.get(username='testuser2')

        # Устанавливаем пароль, который можно использовать для входа
        self.user1.set_password('testpass123')
        self.user1.save()
        self.user2.set_password('testpass123')
        self.user2.save()

    def test_users_list(self):
        """Тест чтения списка пользователей."""
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser1')
        self.assertContains(response, 'testuser2')

    def test_user_registration(self):
        """Тест создания нового пользователя."""
        user_count = User.objects.count()
        registration_data = {
            'username': 'newuser',
            'password1': 'strong_test_pass123',
            'password2': 'strong_test_pass123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }

        response = self.client.post(
            reverse('user_create'),
            data=registration_data,
            follow=True
        )

        # Проверяем успешный редирект на страницу входа
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что пользователь был создан
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Проверяем сообщение об успешной регистрации
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно создан')

    def test_user_update(self):
        """Тест обновления профиля пользователя."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        # Данные для обновления
        update_data = {
            'username': 'updateduser1',
            'first_name': 'Updated',
            'last_name': 'User'
        }

        response = self.client.post(
            reverse('user_update', args=[self.user1.id]),
            data=update_data,
            follow=True
        )

        # Проверяем успешный редирект
        self.assertRedirects(response, reverse('users'))

        # Проверяем, что данные обновились
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser1')
        self.assertEqual(self.user1.first_name, 'Updated')

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_update_permission(self):
        """Тест прав доступа: пользователь может редактировать
        только свой профиль."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        # Пытаемся обновить профиль testuser2
        update_data = {
            'username': 'hacked_user',
            'first_name': 'Hacked',
            'last_name': 'User'
        }

        response = self.client.post(
            reverse('user_update', args=[self.user2.id]),
            data=update_data,
            follow=True
        )

        # Проверяем редирект на главную страницу
        self.assertRedirects(response, reverse('index'))

        # Проверяем, что данные НЕ обновились
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.username, 'testuser2')

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'У вас нет прав для изменения другого пользователя'
        )

    def test_user_delete(self):
        """Тест удаления пользователя."""
        # Авторизуемся как testuser1
        login_successful = self.client.login(username='testuser1',
                                             password='testpass123')
        self.assertTrue(login_successful, "Не удалось войти в систему")

        # Проверяем, что пользователь действительно аутентифицирован
        response = self.client.get(reverse('users'))
        self.assertEqual(response.context['user'].username, 'testuser1')

        user_count = User.objects.count()

        response = self.client.post(
            reverse('user_delete', args=[self.user1.id]),
            follow=True
        )

        # Проверяем успешный редирект
        self.assertRedirects(response, reverse('users'))

        # Проверяем, что пользователь был удален
        self.assertEqual(User.objects.count(), user_count - 1)
        self.assertFalse(User.objects.filter(username='testuser1').exists())

        # Проверяем сообщение
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

    def test_user_delete_permission(self):
        """Тест прав доступа: пользователь может удалить
        только свой аккаунт."""
        # Авторизуемся как testuser1
        self.client.login(username='testuser1', password='testpass123')

        user_count = User.objects.count()

        # Пытаемся удалить testuser2
        response = self.client.post(
            reverse('user_delete', args=[self.user2.id]),
            follow=True
        )

        # Проверяем редирект
        self.assertRedirects(response, reverse('login'))

        # Проверяем, что пользователь НЕ был удален
        self.assertEqual(User.objects.count(), user_count)
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Вы не авторизованы! Пожалуйста, выполните вход.'
        )


class StatusCRUDTestCase(TestCase):
    fixtures = ['task_manager/fixtures/statuses.json']

    def setUp(self):
        self.client = Client()
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Login for CRUD operations
        self.client.login(username='testuser', password='testpass123')
        self.status1 = Status.objects.get(name='new')
        self.status2 = Status.objects.get(name='in progress')
        self.status3 = Status.objects.get(name='done')

    def test_status_list(self):
        """Тест чтения списка статусов."""
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'new')
        self.assertContains(response, 'in progress')
        self.assertContains(response, 'done')

    def test_status_create(self):
        """Тест создания нового статуса."""
        response = self.client.post(
            reverse('status_create'),
            data={'name': 'new_status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Status.objects.count(), 4)
        self.assertTrue(Status.objects.filter(name='new_status').exists())

    def test_status_update(self):
        """Тест обновления статуса."""
        response = self.client.post(
            reverse('status_update', args=[self.status1.id]),
            data={'name': 'updated_status'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'updated_status')

    def test_status_delete(self):
        """Тест удаления статуса."""
        response = self.client.post(
            reverse('status_delete', args=[self.status1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('statuses'))
        self.assertEqual(Status.objects.count(), 2)
        self.assertFalse(Status.objects.filter(id=self.status1.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_status_delete_permission(self):
        """Тест прав доступа: пользователь может удалить
        только свой статус."""
        # Logout first
        self.client.logout()

        response = self.client.post(
            reverse('status_delete', args=[self.status1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Status.objects.count(), 3)
        self.assertTrue(Status.objects.filter(id=self.status1.id).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_status_update_permission(self):
        """Test that unauthorized users cannot update statuses."""
        # Logout first
        self.client.logout()

        # Try to update a status without being logged in
        update_data = {
            'name': 'unauthorized_update'
        }

        # Get initial status value to verify it doesn't change
        original_name = self.status1.name

        response = self.client.post(
            reverse('status_update', args=[self.status1.id]),
            data=update_data,
            follow=True
        )

        # Check redirect to login page
        self.assertRedirects(response, reverse('login'))
        # Verify status was not updated
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, original_name)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')
