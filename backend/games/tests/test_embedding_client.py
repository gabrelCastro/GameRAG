from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from games.infrastructure.embedding_client import EMBEDDING_DIMENSIONS, EMBEDDING_MODEL, EmbeddingClient


class EmbeddingClientTests(SimpleTestCase):
    @override_settings(OPENAI_API_KEY='test-api-key')
    def test_generate_requests_configured_model_and_dimensions(self):
        openai_instance = Mock()
        openai_instance.embeddings.create.return_value = SimpleNamespace(
            data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])]
        )

        with patch('games.infrastructure.embedding_client.OpenAI', return_value=openai_instance) as openai:
            result = EmbeddingClient().generate('texto do jogo')

        self.assertEqual(result, [0.1, 0.2, 0.3])
        openai.assert_called_once_with(api_key='test-api-key')
        openai_instance.embeddings.create.assert_called_once_with(
            input='texto do jogo',
            model=EMBEDDING_MODEL,
            dimensions=EMBEDDING_DIMENSIONS,
        )
