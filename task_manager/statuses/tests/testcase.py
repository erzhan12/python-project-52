from django.test import Client, TestCase

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = ['test_users.json', 'test_statuses.json']

    def setUp(self):
        self.client = Client()

        self.status1 = Status.objects.get(id=1)
        self.status2 = Status.objects.get(id=2)

        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.status_count = Status.objects.count()

        self.valid_status_data = {
            'name': 'New',
        }

        self.update_status_data = {
            'name': 'In testing',
        }