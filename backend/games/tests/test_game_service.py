from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from games.application.game_service import GameService
from games.models import Game


class GameServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = GameService.__new__(GameService)
        self.service._embedding_client = Mock()

    def _game(self, **overrides):
        game = SimpleNamespace(
            pk=1,
            title='Hades',
            description='Roguelike de ação.',
            genre='Action',
            platform='PC',
            developer='Supergiant Games',
            tags=['Roguelike', 'Mythology'],
            embedding=None,
            save=Mock(),
        )
        for key, value in overrides.items():
            setattr(game, key, value)
        return game

    def test_build_embedding_text_uses_search_relevant_fields(self):
        text = self.service._build_embedding_text(self._game())

        self.assertIn('Hades', text)
        self.assertIn('Roguelike de ação.', text)
        self.assertIn('Gênero: Action', text)
        self.assertIn('Plataforma: PC', text)
        self.assertIn('Desenvolvedor: Supergiant Games', text)
        self.assertIn('Tags: Roguelike, Mythology', text)

    def test_build_embedding_text_handles_empty_tags(self):
        text = self.service._build_embedding_text(self._game(tags=[]))

        self.assertIn('Tags:', text)
        self.assertNotIn('None', text)
        self.assertNotIn('[]', text)

    def test_update_embedding_generates_and_persists_embedding(self):
        game = self._game()
        self.service._embedding_client.generate.return_value = [0.1, 0.2, 0.3]

        self.service._update_embedding(game)

        self.assertEqual(game.embedding, [0.1, 0.2, 0.3])
        game.save.assert_called_once_with(update_fields=['embedding'])

    def test_update_embedding_logs_and_does_not_raise_when_provider_fails(self):
        game = self._game()
        self.service._embedding_client.generate.side_effect = RuntimeError('provider unavailable')

        with patch('games.application.game_service.logger') as logger:
            self.service._update_embedding(game)

        logger.exception.assert_called_once_with('Falha ao gerar embedding para o jogo id=%s', game.pk)
        game.save.assert_not_called()

    def test_create_saves_serializer_and_updates_embedding(self):
        serializer = Mock()
        game = self._game()
        serializer.save.return_value = game

        with patch.object(self.service, '_update_embedding') as update_embedding:
            result = self.service.create(serializer)

        self.assertIs(result, game)
        serializer.save.assert_called_once_with()
        update_embedding.assert_called_once_with(game)

    def test_update_saves_serializer_and_updates_embedding(self):
        serializer = Mock()
        game = self._game()
        serializer.save.return_value = game

        with patch.object(self.service, '_update_embedding') as update_embedding:
            result = self.service.update(serializer)

        self.assertIs(result, game)
        serializer.save.assert_called_once_with()
        update_embedding.assert_called_once_with(game)

    def test_delete_delegates_to_model_instance(self):
        game = self._game()
        game.delete = Mock()

        self.service.delete(game)

        game.delete.assert_called_once_with()

    def test_get_queryset_returns_all_games(self):
        with patch('games.application.game_service.Game.objects') as objects:
            objects.all.return_value = ['game']

            result = self.service.get_queryset()

        self.assertEqual(result, ['game'])
        objects.all.assert_called_once_with()

    def test_get_by_id_uses_404_lookup(self):
        with patch('games.application.game_service.get_object_or_404', return_value='game') as get_object_or_404:
            result = self.service.get_by_id(123)

        self.assertEqual(result, 'game')
        get_object_or_404.assert_called_once_with(Game, pk=123)
