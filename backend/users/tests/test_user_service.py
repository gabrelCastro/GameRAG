from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import SimpleTestCase

from users.application.user_service import UserService


class UserServiceTests(SimpleTestCase):
    def test_register_creates_non_staff_user_with_hashed_password_flow(self):
        created_user = User(username='ana', email='ana@example.com')

        with patch('users.application.user_service.User.objects.create_user', return_value=created_user) as create_user:
            result = UserService().register(
                username='ana',
                email='ana@example.com',
                password='senha1234',
            )

        self.assertIs(result, created_user)
        create_user.assert_called_once_with(
            username='ana',
            email='ana@example.com',
            password='senha1234',
            is_staff=False,
        )
