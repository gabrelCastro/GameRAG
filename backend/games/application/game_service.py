import logging

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from games.infrastructure.embedding_client import EmbeddingClient
from games.models import Game

logger = logging.getLogger(__name__)


class GameService:
    def __init__(self):
        self._embedding_client = EmbeddingClient()

    def get_queryset(self) -> QuerySet[Game]:
        return Game.objects.all()

    def get_by_id(self, game_id: int) -> Game:
        return get_object_or_404(Game, pk=game_id)

    def create(self, serializer) -> Game:
        game = serializer.save()
        self._update_embedding(game)
        return game

    def update(self, serializer) -> Game:
        game = serializer.save()
        self._update_embedding(game)
        return game

    def delete(self, instance: Game) -> None:
        instance.delete()

    def _build_embedding_text(self, game: Game) -> str:
        tags = ', '.join(game.tags) if game.tags else ''
        return (
            f"{game.title}. {game.description}. "
            f"Gênero: {game.genre}. Plataforma: {game.platform}. "
            f"Desenvolvedor: {game.developer}. Tags: {tags}."
        )

    def _update_embedding(self, game: Game) -> None:
        try:
            text = self._build_embedding_text(game)
            game.embedding = self._embedding_client.generate(text)
            game.save(update_fields=['embedding'])
        except Exception:
            logger.exception('Falha ao gerar embedding para o jogo id=%s', game.pk)
