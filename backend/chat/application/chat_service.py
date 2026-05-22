import logging

from django.conf import settings
from openai import OpenAI

from games.application.recommendation_service import RecommendationService
from games.infrastructure.embedding_client import EmbeddingClient
from games.models import Game

logger = logging.getLogger(__name__)

_CHAT_MODEL = 'gpt-4o-mini'
_RAG_LIMIT = 5

_SYSTEM_PROMPT = (
    "Você é um assistente especializado em recomendações de videogames. "
    "Responda em português, de forma amigável e direta. "
    "Use apenas as informações dos jogos fornecidos no contexto para embasar sua resposta. "
    "Se os jogos disponíveis não forem relevantes para a pergunta, diga isso honestamente "
    "em vez de inventar informações."
)


class ChatService:
    def __init__(self):
        self._embedding_client = EmbeddingClient()
        self._recommendation_service = RecommendationService()
        self._openai = OpenAI(api_key=settings.OPENAI_API_KEY)

    def answer(self, question: str) -> dict:
        embedding = self._embedding_client.generate(question)
        games = list(self._recommendation_service.find_similar_games(embedding, limit=_RAG_LIMIT))
        context = self._build_context(games)
        answer_text = self._call_llm(question, context)
        return {'answer': answer_text, 'games': games}

    def _build_context(self, games: list[Game]) -> str:
        if not games:
            return 'Nenhum jogo encontrado no catálogo.'
        parts = []
        for g in games:
            tags = ', '.join(g.tags) if g.tags else 'sem tags'
            parts.append(
                f"- {g.title} ({g.platform}): {g.description} "
                f"[Gênero: {g.genre} | Nota: {g.rating}/10 | Preço: R${g.price} | Tags: {tags}]"
            )
        return '\n'.join(parts)

    def _call_llm(self, question: str, context: str) -> str:
        user_message = (
            f"Pergunta do usuário: {question}\n\n"
            f"Jogos disponíveis no catálogo:\n{context}"
        )
        response = self._openai.chat.completions.create(
            model=_CHAT_MODEL,
            messages=[
                {'role': 'system', 'content': _SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content
