from django.core.management.base import BaseCommand

from games.infrastructure.embedding_client import EmbeddingClient
from games.models import Game


class Command(BaseCommand):
    help = 'Gera embeddings para jogos que ainda não os possuem.'

    def handle(self, *args, **options):
        client = EmbeddingClient()
        games = list(Game.objects.filter(embedding=None))

        if not games:
            self.stdout.write('Todos os jogos já possuem embeddings.')
            return

        total = len(games)
        self.stdout.write(f'Gerando embeddings para {total} jogo(s)...')

        for i, game in enumerate(games, 1):
            try:
                text = self._build_text(game)
                game.embedding = client.generate(text)
                game.save(update_fields=['embedding'])
                self.stdout.write(f'  [{i}/{total}] {game.title}')
            except Exception as exc:
                self.stderr.write(f'  Erro em "{game.title}": {exc}')

        self.stdout.write(self.style.SUCCESS('Concluído.'))

    def _build_text(self, game: Game) -> str:
        tags = ', '.join(game.tags) if game.tags else ''
        return (
            f"{game.title}. {game.description}. "
            f"Gênero: {game.genre}. Plataforma: {game.platform}. "
            f"Desenvolvedor: {game.developer}. Tags: {tags}."
        )
