from games.models import GameFavorite, GameLibraryEntry, GameReview


class UserGameService:
    def list_reviews(self, game):
        return game.reviews.select_related('user').all()

    def get_user_review(self, game, user):
        return GameReview.objects.filter(game=game, user=user).first()

    def save_review(self, serializer, game, user):
        return serializer.save(game=game, user=user)

    def delete_review(self, game, user) -> int:
        deleted_count, _ = GameReview.objects.filter(game=game, user=user).delete()
        return deleted_count

    def list_favorites(self, user):
        return GameFavorite.objects.select_related('game').filter(user=user)

    def add_favorite(self, game, user):
        favorite, created = GameFavorite.objects.get_or_create(game=game, user=user)
        return favorite, created

    def remove_favorite(self, game, user) -> int:
        deleted_count, _ = GameFavorite.objects.filter(game=game, user=user).delete()
        return deleted_count

    def list_library(self, user):
        return GameLibraryEntry.objects.select_related('game').filter(user=user)

    def get_library_entry(self, game, user):
        return GameLibraryEntry.objects.filter(game=game, user=user).first()

    def save_library_entry(self, serializer, game, user):
        return serializer.save(game=game, user=user)

    def remove_library_entry(self, game, user) -> int:
        deleted_count, _ = GameLibraryEntry.objects.filter(game=game, user=user).delete()
        return deleted_count
