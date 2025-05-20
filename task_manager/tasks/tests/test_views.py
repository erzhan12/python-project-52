from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskListView(TaskTestCase):
    def test_unauthorized_access_redirects_to_login(self):
        response = self.client.get(reverse_lazy('tasks:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_authorized_access_renders_task_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy('tasks:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertEqual(Task.objects.count(), self.task_count)


class TestTaskFilters(TaskTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user1)

    def test_filter_by_status(self):
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'status': self.status1.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context['tasks'])
        expected_tasks = set(Task.objects.filter(status=self.status1))
        self.assertEqual(tasks, expected_tasks)

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'executor': self.user2.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context['tasks'])
        expected_tasks = set(Task.objects.filter(executor=self.user2))
        self.assertEqual(tasks, expected_tasks)

    def test_filter_by_label(self):
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'label': self.label1.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context['tasks'])
        expected_tasks = set(Task.objects.filter(labels=self.label1))
        self.assertEqual(tasks, expected_tasks)

    def test_task_filter_by_user_own_tasks(self):
        response = self.client.get(
            reverse_lazy('tasks:index'),
            {'user_own_tasks': 'on'}
        )
        self.assertEqual(response.status_code, 200)
        tasks = set(response.context['tasks'])
        expected_tasks = set(Task.objects.filter(author=self.user1))
        self.assertEqual(tasks, expected_tasks)


class TestTaskDetailView(TaskTestCase):
    def test_redirects_unauthorized_user(self):
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_renders_detail_for_authorized_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': self.task1.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertEqual(response.context['task'], self.task1)

    def test_404_for_nonexistent_task(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)


class TestTaskCreateView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(reverse_lazy('tasks:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:create'), data=self.valid_task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_creates_task_for_logged_in_user(self):
        self.client.force_login(self.user1)
        initial_count = Task.objects.count()

        response = self.client.get(reverse_lazy('tasks:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse_lazy('tasks:create'),
            data=self.valid_task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks:index'))
        self.assertEqual(Task.objects.count(), initial_count + 1)


class TestTaskUpdateView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_logged_in_user_can_update_task(self):
        self.client.force_login(self.user1)
        update_data = self.update_task_data.copy()
        update_data['name'] = 'Updated name'

        response = self.client.get(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': self.task1.id}),
            data=update_data
        )
        self.assertRedirects(response, reverse_lazy('tasks:index'))
        updated_task = Task.objects.get(id=self.task1.id)
        self.assertEqual(updated_task.name, update_data['name'])

    def test_other_user_task_update_authorized(self):
        task = self.task1
        self.client.force_login(self.user2)
        update_data = self.valid_task_data.copy()
        update_data.update({
            'name': 'Updated name'
        })

        response = self.client.get(
            reverse_lazy('tasks:update', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')

        response = self.client.post(
            reverse_lazy('tasks:update', kwargs={'pk': task.id}),
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks:index'))
        updated_task = Task.objects.get(id=task.id)
        self.assertEqual(updated_task.name, update_data['name'])


class TestTaskDeleteView(TaskTestCase):
    def test_redirects_unauthenticated_user(self):
        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_owner_can_delete_task(self):
        self.client.force_login(self.user2)
        initial_count = Task.objects.count()

        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': self.task1.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks:index'))
        self.assertEqual(Task.objects.count(), initial_count - 1)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.id)

    def test_non_author_cannot_delete_task(self):
        user = self.user1
        task = self.task1
        self.client.force_login(user)
        initial_count = Task.objects.count()

        response = self.client.get(
            reverse_lazy('tasks:delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks:index'))

        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks:index'))
        self.assertEqual(Task.objects.count(), initial_count)
        unchanged_task = Task.objects.get(id=task.id)
        self.assertEqual(unchanged_task.name, task.name)