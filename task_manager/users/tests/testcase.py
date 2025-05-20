from django.test import Client, TestCase

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ['test_users.json']

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)

        self.user_count = User.objects.count()

        self.valid_user_data = {
            'first_name': 'Arya',
            'last_name': 'Stark',
            'username': 'no_one',
            'password1': 'ValarMorghulis123',
            'password2': 'ValarMorghulis123'
        }

        self.update_user_data = {
            'first_name': 'Sansa',
            'last_name': 'Stark',
            'username': 'lady_winterfell',
            'password1': 'QueenInNorth456',
            'password2': 'QueenInNorth456'
        }