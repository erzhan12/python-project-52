from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelListView(LabelTestCase):
    def test_labels_list_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)

        response = self.client.get(reverse_lazy('labels:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/index.html')
        self.assertEqual(Label.objects.count(), self.label_count)

    def test_labels_list_unauthorized(self):
        response = self.client.get(reverse_lazy('labels:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestLabelCreateView(LabelTestCase):
    def test_label_creation_authorized(self):
        user1 = self.user1
        label_data = self.valid_label_data
        self.client.force_login(user1)
        initial_count = Label.objects.count()

        response = self.client.get(reverse_lazy('labels:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_form.html')

        response = self.client.post(
            reverse_lazy('labels:create'),
            data=label_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels:index'))
        self.assertEqual(Label.objects.count(), initial_count + 1)

    def test_label_creation_unauthorized(self):
        label_data = self.valid_label_data

        response = self.client.get(reverse_lazy('labels:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('labels:create'),
            data=label_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestLabelUpdateView(LabelTestCase):
    def test_label_update_authorized(self):
        user1 = self.user1
        label1 = self.label1
        update_data = self.update_label_data
        self.client.force_login(user1)

        response = self.client.get(
            reverse_lazy('labels:update', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_form.html')

        response = self.client.post(
            reverse_lazy('labels:update', kwargs={'pk': label1.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels:index'))
        updated_label = Label.objects.get(id=label1.id)
        self.assertEqual(updated_label.name, update_data['name'])

    def test_label_update_unauthorized(self):
        label1 = self.label1
        update_data = self.update_label_data

        response = self.client.get(
            reverse_lazy('labels:update', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('labels:update', kwargs={'pk': label1.id}),
            data=update_data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestLabelDeleteView(LabelTestCase):
    def test_label_deletion_authorized(self):
        user1 = self.user1
        label1 = self.label1
        self.client.force_login(user1)
        initial_count = Label.objects.count()

        response = self.client.get(
            reverse_lazy('labels:delete', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_delete.html')

        response = self.client.post(
            reverse_lazy('labels:delete', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels:index'))
        self.assertEqual(Label.objects.count(), initial_count - 1)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=label1.id)

    def test_label_deletion_unauthorized(self):
        label1 = self.label1

        response = self.client.get(
            reverse_lazy('labels:delete', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('labels:delete', kwargs={'pk': label1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))