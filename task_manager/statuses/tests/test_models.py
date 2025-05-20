from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusModel(StatusTestCase):
    def create_test_status(self, **overrides):
        status_data = {
            'name': self.valid_status_data['name'],
        }
        status_data.update(overrides)
        return Status.objects.create(**status_data)

    def test_status_creation(self):
        initial_count = Status.objects.count()
        status = self.create_test_status()
        self.assertEqual(Status.objects.count(), initial_count + 1)

        db_status = Status.objects.get(pk=status.pk)
        self.assertEqual(db_status.name, self.valid_status_data['name'])
        self.assertIsNotNone(db_status.created_at)
        self.assertEqual(str(db_status), self.valid_status_data['name'])

    def test_duplicate_status_name(self):
        self.create_test_status(name=self.valid_status_data['name'])
        with self.assertRaises(Exception):
            self.create_test_status()

    def test_blank_status_name(self):
        status = Status(name='')
        with self.assertRaises(Exception):
            status.full_clean()