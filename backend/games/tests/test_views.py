from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase

from games.interfaces.views import GameViewSet


class SimilarLimitParsingTests(SimpleTestCase):
    def setUp(self):
        self.viewset = GameViewSet.__new__(GameViewSet)

    def _request_with_limit(self, limit):
        query_params = {} if limit is None else {'limit': limit}
        return SimpleNamespace(query_params=query_params)

    def test_uses_default_limit_when_param_is_absent(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit(None))

        self.assertEqual(limit, 10)
        self.assertIsNone(error_response)

    def test_caps_limit_at_50(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit('999'))

        self.assertEqual(limit, 50)
        self.assertIsNone(error_response)

    def test_rejects_non_integer_limit(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit('abc'))

        self.assertIsNone(limit)
        self.assertEqual(error_response.status_code, 400)

    def test_rejects_float_limit(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit('1.5'))

        self.assertIsNone(limit)
        self.assertEqual(error_response.status_code, 400)

    def test_rejects_empty_limit(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit(''))

        self.assertIsNone(limit)
        self.assertEqual(error_response.status_code, 400)

    def test_rejects_limit_less_than_one(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit('0'))

        self.assertIsNone(limit)
        self.assertEqual(error_response.status_code, 400)

    def test_accepts_limit_with_surrounding_spaces(self):
        limit, error_response = self.viewset._parse_similar_limit(self._request_with_limit(' 5 '))

        self.assertEqual(limit, 5)
        self.assertIsNone(error_response)


class SimilarActionTests(SimpleTestCase):
    def setUp(self):
        self.viewset = GameViewSet.__new__(GameViewSet)
        self.viewset._service = Mock()
        self.viewset._recommendation_service = Mock()
        self.viewset.get_serializer = Mock()

    def _request_with_limit(self, limit):
        query_params = {} if limit is None else {'limit': limit}
        return SimpleNamespace(query_params=query_params)

    def test_returns_422_when_game_has_no_embedding(self):
        self.viewset._service.get_by_id.return_value = SimpleNamespace(embedding=None)

        response = self.viewset.similar(self._request_with_limit('abc'), pk=1)

        self.assertEqual(response.status_code, 422)
        self.viewset._recommendation_service.find_similar_to_game.assert_not_called()

    def test_returns_400_for_invalid_limit_when_game_has_embedding(self):
        self.viewset._service.get_by_id.return_value = SimpleNamespace(embedding=[0.1, 0.2])

        response = self.viewset.similar(self._request_with_limit('abc'), pk=1)

        self.assertEqual(response.status_code, 400)
        self.viewset._recommendation_service.find_similar_to_game.assert_not_called()

    def test_serializes_similar_games_with_valid_limit(self):
        game = SimpleNamespace(embedding=[0.1, 0.2])
        similar_games = [SimpleNamespace(pk=2)]
        serializer = SimpleNamespace(data=[{'id': 2}])
        self.viewset._service.get_by_id.return_value = game
        self.viewset._recommendation_service.find_similar_to_game.return_value = similar_games
        self.viewset.get_serializer.return_value = serializer

        response = self.viewset.similar(self._request_with_limit('75'), pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{'id': 2}])
        self.viewset._recommendation_service.find_similar_to_game.assert_called_once_with(game, limit=50)
        self.viewset.get_serializer.assert_called_once_with(similar_games, many=True)
