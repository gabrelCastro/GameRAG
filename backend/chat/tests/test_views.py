from types import SimpleNamespace

from django.test import SimpleTestCase
from rest_framework.permissions import IsAuthenticated

from chat.interfaces.views import ChatView


class ChatViewTests(SimpleTestCase):
    def test_requires_authenticated_user(self):
        self.assertEqual(ChatView.permission_classes, [IsAuthenticated])

    def test_post_returns_current_placeholder_response(self):
        response = ChatView().post(SimpleNamespace(data={'message': 'Quero um RPG'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'answer': 'Em construção.',
                'games': [],
            },
        )
