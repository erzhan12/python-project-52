from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestCustomUserCreationForm(UserTestCase):
    def get_form(self, overrides=None):
        data = self.valid_user_data.copy()
        if overrides:
            data.update(overrides)
        return CustomUserCreationForm(data=data)

    def test_valid_data(self):
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(User.objects.count(), self.user_count + 1)

    def test_missing_fields(self):
        cases = [
            {'username': self.valid_user_data['username']},
            {
                'username': self.valid_user_data['username'],
                'password1': 'test123',  # NOSONAR
            },
            {'first_name': 'Test', 'last_name': 'User'},
        ]

        for data in cases:
            with self.subTest(data=data):
                form = CustomUserCreationForm(data=data)
                self.assertFalse(form.is_valid())

    def test_password_too_short(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data.update({
            'password1': '12',  # NOSONAR
            'password2': '12'   # NOSONAR
        })
        form = CustomUserCreationForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_invalid_username(self):
        test_cases = [
            '!!!',
            'user#name',
            'user name',
            'x' * 151,
        ]

        for username in test_cases:
            with self.subTest(username=username):
                invalid_data = self.valid_user_data.copy()
                invalid_data['username'] = username
                form = CustomUserCreationForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn('username', form.errors)

    def test_passwords_do_not_match(self):
        form = self.get_form({'password2': 'Different123'})  # NOSONAR
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_empty_strings(self):
        form = self.get_form({
            'first_name': '',
            'last_name': '',
            'username': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_duplicate_username(self):
        form = self.get_form({'username': 'john_snow'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TestCustomUserChangeForm(UserTestCase):
    def get_form(self, overrides=None):
        data = self.update_user_data.copy()
        data.update({
            'password1': data.pop('password1'),
            'password2': data.pop('password2')
        })
        if overrides:
            data.update(overrides)
        return CustomUserChangeForm(data=data, instance=self.user1)

    def test_valid_password_update(self):
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.update_user_data['username'])
        self.assertTrue(user.check_password(
            self.update_user_data['password1']  # NOSONAR
        ))

    def test_passwords_do_not_match(self):
        form = self.get_form({'password2': 'WrongConfirm'})  # NOSONAR
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_short_password(self):
        form = self.get_form({
            'password1': '12',  # NOSONAR
            'password2': '12'   # NOSONAR
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_password_fields(self):
        for case in [
            {'password1': '', 'password2': 'SomePassword'},  # NOSONAR
            {'password1': 'SomePassword', 'password2': ''}   # NOSONAR
        ]:
            with self.subTest(case=case):
                form = self.get_form(case)
                self.assertFalse(form.is_valid())
                self.assertTrue(
                    'password1' in form.errors or 'password2' in form.errors
                )

    def test_update_with_existing_valid_password(self):
        form = self.get_form({
            'password1': 'QueenInNorth456',  # NOSONAR
            'password2': 'QueenInNorth456',  # NOSONAR
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password('QueenInNorth456'))  # NOSONAR