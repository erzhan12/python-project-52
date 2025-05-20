from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelModel(LabelTestCase):
    def create_test_label(self, **overrides):
        label_data = {
            'name': self.valid_label_data['name']
        }
        label_data.update(overrides)
        return Label.objects.create(**label_data)

    def test_label_creation(self):
        initial_count = Label.objects.count()
        label = self.create_test_label()
        self.assertEqual(Label.objects.count(), initial_count + 1)
        self.assertEqual(label.name, self.valid_label_data['name'])
        self.assertEqual(str(label), self.valid_label_data['name'])

    def test_duplicate_label_name(self):
        with self.assertRaises(Exception):
            self.create_test_label(name=self.label1.name)

    def test_blank_label_name(self):
        label = Label(name='')
        with self.assertRaises(Exception):
            label.full_clean()