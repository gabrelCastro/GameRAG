from unittest.mock import Mock, patch

from django.core.management.base import CommandError
from django.test import SimpleTestCase

from users.management.commands.create_admin_user import Command


class CreateAdminUserCommandTests(SimpleTestCase):
    def setUp(self):
        self.command = Command()
        self.user = Mock()
        self.user.email = ''
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.has_usable_password.return_value = False
        self.user.set_password = Mock()
        self.user.save = Mock()

        self.user_model = Mock()
        self.user_model.objects.get_or_create.return_value = (self.user, True)

    def _run_command(self, **options):
        with patch(
            'users.management.commands.create_admin_user.get_user_model',
            return_value=self.user_model,
        ):
            return self.command.handle(**options)

    def test_creates_admin_user_with_staff_and_superuser_flags(self):
        self._run_command(
            username='admin',
            email='admin@example.com',
            password='senha1234',
            first_name='Ana',
            last_name='Admin',
        )

        self.user_model.objects.get_or_create.assert_called_once_with(
            username='admin',
            defaults={'email': 'admin@example.com'},
        )
        self.assertEqual(self.user.email, 'admin@example.com')
        self.assertEqual(self.user.first_name, 'Ana')
        self.assertEqual(self.user.last_name, 'Admin')
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)
        self.assertTrue(self.user.is_active)
        self.user.set_password.assert_called_once_with('senha1234')
        self.user.save.assert_called_once_with()

    def test_keeps_existing_password_when_user_already_has_one(self):
        self.user_model.objects.get_or_create.return_value = (self.user, False)
        self.user.has_usable_password.return_value = True

        self._run_command(
            username='admin',
            email='admin@example.com',
            password='senha1234',
        )

        self.user.set_password.assert_not_called()
        self.user.save.assert_called_once_with()
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

    def test_requires_username(self):
        with self.assertRaises(CommandError):
            self._run_command(password='senha1234')

    def test_requires_password(self):
        with self.assertRaises(CommandError):
            self._run_command(username='admin')