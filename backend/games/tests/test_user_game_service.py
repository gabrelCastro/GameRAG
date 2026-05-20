from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from games.application.user_game_service import UserGameService


class UserGameServiceTests(SimpleTestCase):
    def setUp(self):
        self.service = UserGameService()
        self.game = Mock()
        self.user = Mock()

    def test_list_reviews_uses_game_related_manager(self):
        reviews = self.game.reviews.select_related.return_value.all.return_value

        result = self.service.list_reviews(self.game)

        self.assertIs(result, reviews)
        self.game.reviews.select_related.assert_called_once_with('user')

    def test_get_user_review_returns_first_matching_review(self):
        with patch('games.application.user_game_service.GameReview.objects') as objects:
            objects.filter.return_value.first.return_value = 'review'

            result = self.service.get_user_review(self.game, self.user)

        self.assertEqual(result, 'review')
        objects.filter.assert_called_once_with(game=self.game, user=self.user)

    def test_save_review_adds_game_and_user_to_serializer_save(self):
        serializer = Mock()
        serializer.save.return_value = 'review'

        result = self.service.save_review(serializer, self.game, self.user)

        self.assertEqual(result, 'review')
        serializer.save.assert_called_once_with(game=self.game, user=self.user)

    def test_delete_review_returns_deleted_count(self):
        with patch('games.application.user_game_service.GameReview.objects') as objects:
            objects.filter.return_value.delete.return_value = (1, {})

            result = self.service.delete_review(self.game, self.user)

        self.assertEqual(result, 1)
        objects.filter.assert_called_once_with(game=self.game, user=self.user)

    def test_add_favorite_returns_favorite_and_created_flag(self):
        with patch('games.application.user_game_service.GameFavorite.objects') as objects:
            objects.get_or_create.return_value = ('favorite', True)

            result = self.service.add_favorite(self.game, self.user)

        self.assertEqual(result, ('favorite', True))
        objects.get_or_create.assert_called_once_with(game=self.game, user=self.user)

    def test_list_favorites_filters_by_user(self):
        with patch('games.application.user_game_service.GameFavorite.objects') as objects:
            objects.select_related.return_value.filter.return_value = ['favorite']

            result = self.service.list_favorites(self.user)

        self.assertEqual(result, ['favorite'])
        objects.select_related.assert_called_once_with('game')
        objects.select_related.return_value.filter.assert_called_once_with(user=self.user)

    def test_save_library_entry_adds_game_and_user_to_serializer_save(self):
        serializer = Mock()
        serializer.save.return_value = 'entry'

        result = self.service.save_library_entry(serializer, self.game, self.user)

        self.assertEqual(result, 'entry')
        serializer.save.assert_called_once_with(game=self.game, user=self.user)

    def test_remove_library_entry_returns_deleted_count(self):
        with patch('games.application.user_game_service.GameLibraryEntry.objects') as objects:
            objects.filter.return_value.delete.return_value = (1, {})

            result = self.service.remove_library_entry(self.game, self.user)

        self.assertEqual(result, 1)
        objects.filter.assert_called_once_with(game=self.game, user=self.user)
