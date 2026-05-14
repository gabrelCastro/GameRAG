from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from games.application.recommendation_service import RecommendationService


class RecommendationServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = RecommendationService()

    def test_find_similar_to_game_returns_empty_queryset_when_embedding_is_missing(self):
        with patch('games.application.recommendation_service.Game.objects') as objects:
            objects.none.return_value = 'empty-queryset'

            result = self.service.find_similar_to_game(SimpleNamespace(embedding=None))

        self.assertEqual(result, 'empty-queryset')
        objects.none.assert_called_once_with()

    def test_find_similar_to_game_excludes_source_game_before_ordering(self):
        game = SimpleNamespace(pk=7, embedding=[0.1, 0.2])

        with (
            patch('games.application.recommendation_service.CosineDistance', return_value='distance-expression') as cosine_distance,
            patch('games.application.recommendation_service.Game.objects') as objects,
        ):
            first_exclude = MagicMock()
            second_exclude = MagicMock()
            ordered = MagicMock()
            objects.exclude.return_value = first_exclude
            first_exclude.exclude.return_value = second_exclude
            second_exclude.order_by.return_value = ordered
            ordered.__getitem__.return_value = ['similar-game']

            result = self.service.find_similar_to_game(game, limit=3)

        self.assertEqual(result, ['similar-game'])
        objects.exclude.assert_called_once_with(embedding=None)
        first_exclude.exclude.assert_called_once_with(pk=7)
        cosine_distance.assert_called_once_with('embedding', game.embedding)
        second_exclude.order_by.assert_called_once_with('distance-expression')
        ordered.__getitem__.assert_called_once_with(slice(None, 3, None))

    def test_find_similar_games_orders_by_cosine_distance_and_applies_limit(self):
        embedding = [0.1, 0.2]

        with (
            patch('games.application.recommendation_service.CosineDistance', return_value='distance-expression') as cosine_distance,
            patch('games.application.recommendation_service.Game.objects') as objects,
        ):
            excluded = MagicMock()
            ordered = MagicMock()
            objects.exclude.return_value = excluded
            excluded.order_by.return_value = ordered
            ordered.__getitem__.return_value = ['game']

            result = self.service.find_similar_games(embedding, limit=1)

        self.assertEqual(result, ['game'])
        objects.exclude.assert_called_once_with(embedding=None)
        cosine_distance.assert_called_once_with('embedding', embedding)
        excluded.order_by.assert_called_once_with('distance-expression')
        ordered.__getitem__.assert_called_once_with(slice(None, 1, None))
