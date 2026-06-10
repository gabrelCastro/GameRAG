from django.contrib.auth.models import AbstractBaseUser
from django.db.models import QuerySet

from games.models import Game, GameFavorite, GameLibraryEntry, GameReview


class UserGameService:
    def list_reviews(self, game: Game) -> QuerySet[GameReview]:
        return game.reviews.select_related('user').all()

    def get_user_review(self, game: Game, user: AbstractBaseUser) -> GameReview | None:
        return GameReview.objects.filter(game=game, user=user).first()

    def save_review(self, serializer, game: Game, user: AbstractBaseUser) -> GameReview:
        return serializer.save(game=game, user=user)

    def delete_review(self, game: Game, user: AbstractBaseUser) -> int:
        deleted_count, _ = GameReview.objects.filter(game=game, user=user).delete()
        return deleted_count

    def list_favorites(self, user: AbstractBaseUser) -> QuerySet[GameFavorite]:
        return GameFavorite.objects.select_related('game').filter(user=user)

    def add_favorite(self, game: Game, user: AbstractBaseUser) -> tuple[GameFavorite, bool]:
        favorite, created = GameFavorite.objects.get_or_create(game=game, user=user)
        return favorite, created

    def remove_favorite(self, game: Game, user: AbstractBaseUser) -> int:
        deleted_count, _ = GameFavorite.objects.filter(game=game, user=user).delete()
        return deleted_count

    def list_library(self, user: AbstractBaseUser) -> QuerySet[GameLibraryEntry]:
        return GameLibraryEntry.objects.select_related('game').filter(user=user)

    def get_library_entry(self, game: Game, user: AbstractBaseUser) -> GameLibraryEntry | None:
        return GameLibraryEntry.objects.filter(game=game, user=user).first()

    def save_library_entry(self, serializer, game: Game, user: AbstractBaseUser) -> GameLibraryEntry:
        return serializer.save(game=game, user=user)

    def remove_library_entry(self, game: Game, user: AbstractBaseUser) -> int:
        deleted_count, _ = GameLibraryEntry.objects.filter(game=game, user=user).delete()
        return deleted_count
