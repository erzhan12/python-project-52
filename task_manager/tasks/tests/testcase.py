from django.test import Client, TestCase

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    fixtures = ['test_users.json',
                'test_statuses.json',
                'test_labels.json',
                'test_tasks.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status1 = Status.objects.get(pk=1)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.task1.labels.set([self.label1])
        self.task2.labels.set([self.label1, self.label2])

        self.task_count = Task.objects.count()

        self.valid_task_data = {
            'name': 'Hold the North',
            'description': 'Secure Winterfell before winter comes.',
            'status': self.status1.id,
            'executor': self.user1.id,
            'labels': [self.label1.id, self.label2.id]
        }

        self.update_task_data = {
            'name': 'Dracarys',
            'description': 'Daenerys commands Drogon to attack.',
            'status': self.status1.id,
            'executor': self.user2.id,
            'labels': [self.label1.id, self.label2.id]
        }