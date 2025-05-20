from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestUserListView(UserTestCase):
    def test_user_list(self):
        response = self.client.get(reverse_lazy('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(User.objects.count(), self.user_count)


class TestUserCreateView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse_lazy('users:create')
        self.redirect_url = reverse_lazy('login')

    def test_get_create_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration_form.html')

    def test_user_creation(self):
        initial_count = User.objects.count()
        response = self.client.post(self.url, data=self.valid_user_data)

        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)


class TestUserDeleteView(UserTestCase):
    def test_user_deletion_unauthorized(self):
        response = self.client.get(reverse_lazy(
            'users:delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(reverse_lazy(
            'users:delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_deletion_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)
        initial_count = User.objects.count()

        response = self.client.get(reverse_lazy(
            'users:delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_delete.html')

        response = self.client.post(reverse_lazy(
            'users:delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))
        self.assertEqual(User.objects.count(), initial_count - 1)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user1.id)

    def test_other_user_deletion_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)

        response = self.client.get(reverse_lazy(
            'users:delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))

        response = self.client.post(
            reverse_lazy('users:delete', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, user1.username)


class TestUserUpdateView(UserTestCase):
    def test_user_update_unauthorized(self):
        user1 = self.user1

        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('users:update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_user_self_update_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)

        update_data = {
            'first_name': 'Aegon',
            'last_name': 'Targaryen',
            'username': 'aegon_t',
            'password1': 'Dracarys321',
            'password2': 'Dracarys321',
        }

        response = self.client.get(reverse_lazy(
            'users:update', kwargs={'pk': user1.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration_form.html')

        response = self.client.post(
            reverse_lazy('users:update', kwargs={'pk': user1.id}),
            update_data
        )

        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))

        updated_user = User.objects.get(id=user1.id)
        self.assertEqual(updated_user.username, 'aegon_t')
        self.assertEqual(updated_user.first_name, 'Aegon')
        self.assertEqual(updated_user.last_name, 'Targaryen')

    def test_other_user_update_authorized(self):
        user1 = self.user1
        user2 = self.user2
        self.client.force_login(user2)

        update_data = {
            'first_name': 'Petyr',
            'last_name': 'Baelish',
            'username': 'chaos_is_a_ladder',
            'password1': 'ILoveCatelyn',
            'password2': 'ILoveCatelyn',
        }

        response = self.client.get(
            reverse_lazy('users:update', kwargs={'pk': user1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))

        response = self.client.post(
            reverse_lazy('users:update', kwargs={'pk': user1.id}),
            update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users:index'))
        unchanged_user = User.objects.get(id=user1.id)
        self.assertEqual(unchanged_user.username, 'john_snow')