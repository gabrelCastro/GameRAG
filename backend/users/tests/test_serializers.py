from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import SimpleTestCase
from rest_framework import serializers

from users.interfaces.serializers import RegisterSerializer


class RegisterSerializerTests(SimpleTestCase):
    def _valid_payload(self, **overrides):
        payload = {
            'username': 'ana',
            'email': 'ana@example.com',
            'password': 'senha1234',
        }
        payload.update(overrides)
        return payload

    def test_password_is_write_only(self):
        serializer = RegisterSerializer(instance=User(username='ana', email='ana@example.com'))

        self.assertNotIn('password', serializer.data)

    def test_id_is_read_only(self):
        serializer = RegisterSerializer()

        self.assertTrue(serializer.fields['id'].read_only)

    def test_rejects_password_shorter_than_eight_chars(self):
        serializer = RegisterSerializer()

        with self.assertRaises(serializers.ValidationError):
            serializer.fields['password'].run_validation('1234567')

    def test_accepts_password_with_exact_minimum_length(self):
        serializer = RegisterSerializer()

        self.assertEqual(serializer.fields['password'].run_validation('12345678'), '12345678')

    def test_rejects_duplicate_email(self):
        serializer = RegisterSerializer()

        with patch('users.interfaces.serializers.User.objects.filter') as user_filter:
            user_filter.return_value.exists.return_value = True

            with self.assertRaises(serializers.ValidationError):
                serializer.validate_email('ana@example.com')

    def test_accepts_unique_email(self):
        serializer = RegisterSerializer()

        with patch('users.interfaces.serializers.User.objects.filter') as user_filter:
            user_filter.return_value.exists.return_value = False

            result = serializer.validate_email('ana@example.com')

        self.assertEqual(result, 'ana@example.com')

    def test_save_delegates_user_creation_to_application_service(self):
        user = User(username='ana', email='ana@example.com')

        with patch('users.interfaces.serializers.User.objects.filter') as user_filter:
            user_filter.return_value.exists.return_value = False
            serializer = RegisterSerializer(data=self._valid_payload())
            self.assertTrue(serializer.is_valid(), serializer.errors)

        with patch('users.application.user_service.UserService.register', return_value=user) as register:
            result = serializer.save()

        self.assertIs(result, user)
        register.assert_called_once_with(
            username='ana',
            email='ana@example.com',
            password='senha1234',
        )
