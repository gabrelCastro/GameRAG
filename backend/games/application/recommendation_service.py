from django.db.models import QuerySet
from pgvector.django import CosineDistance

from games.models import Game


class RecommendationService:
    DEFAULT_LIMIT = 10

    def find_similar_games(self, embedding: list[float], limit: int = DEFAULT_LIMIT) -> QuerySet[Game]:
        return (
            Game.objects
            .exclude(embedding=None)
            .order_by(CosineDistance('embedding', embedding))[:limit]
        )

    def find_similar_to_game(self, game: Game, limit: int = DEFAULT_LIMIT) -> QuerySet[Game]:
        if game.embedding is None:
            return Game.objects.none()
        return (
            Game.objects
            .exclude(embedding=None)
            .exclude(pk=game.pk)
            .order_by(CosineDistance('embedding', game.embedding))[:limit]
        )
