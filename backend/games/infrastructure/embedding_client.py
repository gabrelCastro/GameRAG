import logging

from django.conf import settings
from openai import OpenAI

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_DIMENSIONS = 1536


class EmbeddingClient:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, text: str) -> list[float]:
        response = self._client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL,
            dimensions=EMBEDDING_DIMENSIONS,
        )
        return response.data[0].embedding
