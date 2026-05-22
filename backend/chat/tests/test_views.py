from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from chat.interfaces.views import ChatView


class ChatViewPermissionTests(SimpleTestCase):
    def test_requires_authenticated_user(self):
        self.assertEqual(ChatView.permission_classes, [IsAuthenticated])


class ChatViewPostTests(SimpleTestCase):
    def _make_request(self, data):
        return SimpleNamespace(data=data)

    def test_missing_message_returns_400(self):
        response = ChatView().post(self._make_request({}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_empty_message_returns_400(self):
        response = ChatView().post(self._make_request({'message': '   '}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('chat.interfaces.views.GameSerializer')
    @patch('chat.interfaces.views.ChatService')
    def test_returns_answer_and_serialized_games(self, MockChatService, MockGameSerializer):
        fake_game = MagicMock()
        MockChatService.return_value.answer.return_value = {
            'answer': 'Recomendo Hollow Knight!',
            'games': [fake_game],
        }
        MockGameSerializer.return_value.data = [{'id': 1, 'title': 'Hollow Knight'}]

        response = ChatView().post(self._make_request({'message': 'Quero um metroidvania'}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], 'Recomendo Hollow Knight!')
        self.assertEqual(response.data['games'], [{'id': 1, 'title': 'Hollow Knight'}])
        MockChatService.return_value.answer.assert_called_once_with('Quero um metroidvania')
        MockGameSerializer.assert_called_once_with([fake_game], many=True)

    @patch('chat.interfaces.views.ChatService')
    def test_service_exception_returns_500(self, MockChatService):
        MockChatService.return_value.answer.side_effect = RuntimeError('OpenAI fora do ar')

        response = ChatView().post(self._make_request({'message': 'Qualquer coisa'}))

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
