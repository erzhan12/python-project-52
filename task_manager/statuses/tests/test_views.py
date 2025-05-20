from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusListView(StatusTestCase):
    def test_statuses_list_authorized(self):
        user1 = self.user1

        self.client.force_login(user1)
        response = self.client.get(reverse_lazy('statuses:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertEqual(Status.objects.count(), self.status_count)

    def test_statuses_list_unauthorized(self):
        response = self.client.get(reverse_lazy('statuses:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestStatusCreateView(StatusTestCase):
    def test_status_creation_authorized(self):
        user1 = self.user1
        status_data = self.valid_status_data
        initial_count = Status.objects.count()

        self.client.force_login(user1)

        response = self.client.get(reverse_lazy('statuses:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_form.html')

        response = self.client.post(
            reverse_lazy('statuses:create'),
            data=status_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses:index'))
        self.assertEqual(Status.objects.count(), initial_count + 1)

    def test_status_creation_unauthorized(self):
        status_data = self.valid_status_data

        response = self.client.get(reverse_lazy('statuses:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('statuses:create'),
            data=status_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestStatusUpdateView(StatusTestCase):
    def test_status_update_authorized(self):
        user1 = self.user1
        status = self.status1
        update_data = self.update_status_data

        self.client.force_login(user1)

        response = self.client.get(
            reverse_lazy('statuses:update', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_form.html')

        response = self.client.post(
            reverse_lazy('statuses:update', kwargs={'pk': status.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses:index'))

        updated_status = Status.objects.get(id=status.id)
        self.assertEqual(updated_status.name, update_data['name'])

    def test_status_update_unauthorized(self):
        status = self.status1
        update_data = self.update_status_data

        response = self.client.get(
            reverse_lazy('statuses:update', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('statuses:update', kwargs={'pk': status.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestStatusDeleteView(StatusTestCase):
    def test_status_deletion_authorized(self):
        user1 = self.user1
        status = self.status1
        initial_count = Status.objects.count()

        self.client.force_login(user1)

        response = self.client.get(
            reverse_lazy('statuses:delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_delete.html')

        response = self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses:index'))
        self.assertEqual(Status.objects.count(), initial_count - 1)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=status.id)

    def test_status_deletion_unauthorized(self):
        status = self.status1

        response = self.client.get(
            reverse_lazy('statuses:delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('statuses:delete', kwargs={'pk': status.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))