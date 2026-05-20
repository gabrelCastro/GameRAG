from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from games.application.game_service import GameService
from games.application.recommendation_service import RecommendationService
from games.application.user_game_service import UserGameService
from games.interfaces.serializers import (
    GameFavoriteSerializer,
    GameLibraryEntrySerializer,
    GameReviewSerializer,
    GameSerializer,
)


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    admin_only_actions = {'create', 'update', 'partial_update', 'destroy'}
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre', 'platform', 'developer', 'publisher']
    ordering_fields = ['title', 'price', 'rating', 'release_date']
    ordering = ['title']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = GameService()
        self._recommendation_service = RecommendationService()
        self._interaction_service = UserGameService()

    def get_permissions(self):
        if self.action in self.admin_only_actions:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return self._service.get_queryset()

    def perform_create(self, serializer):
        self._service.create(serializer)

    def perform_update(self, serializer):
        self._service.update(serializer)

    def perform_destroy(self, instance):
        self._service.delete(instance)

    def _parse_similar_limit(self, request):
        raw_limit = request.query_params.get('limit', RecommendationService.DEFAULT_LIMIT)

        try:
            limit = int(raw_limit)
        except (TypeError, ValueError):
            return None, Response(
                {'detail': 'O parâmetro limit deve ser um número inteiro positivo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if limit < 1:
            return None, Response(
                {'detail': 'O parâmetro limit deve ser maior ou igual a 1.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return min(limit, 50), None

    @action(
        detail=True,
        methods=['get'],
        url_path='similar',
        permission_classes=[IsAuthenticated],
    )
    def similar(self, request, pk=None):
        game = self._service.get_by_id(pk)

        if game.embedding is None:
            return Response(
                {'detail': 'Este jogo ainda não possui embedding gerado.'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        limit, error_response = self._parse_similar_limit(request)
        if error_response is not None:
            return error_response

        similar_games = self._recommendation_service.find_similar_to_game(game, limit=limit)
        serializer = self.get_serializer(similar_games, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path='reviews',
        permission_classes=[IsAuthenticated],
    )
    def reviews(self, request, pk=None):
        game = self._service.get_by_id(pk)

        if request.method == 'GET':
            reviews = self._interaction_service.list_reviews(game)
            serializer = GameReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        review = self._interaction_service.get_user_review(game, request.user)
        serializer = GameReviewSerializer(
            review,
            data=request.data,
            partial=review is not None,
        )
        serializer.is_valid(raise_exception=True)
        self._interaction_service.save_review(serializer, game, request.user)
        return Response(serializer.data, status=status.HTTP_200_OK if review else status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['delete'],
        url_path='reviews/me',
        permission_classes=[IsAuthenticated],
    )
    def delete_my_review(self, request, pk=None):
        game = self._service.get_by_id(pk)
        self._interaction_service.delete_review(game, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        game = self._service.get_by_id(pk)

        if request.method == 'DELETE':
            self._interaction_service.remove_favorite(game, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        favorite, created = self._interaction_service.add_favorite(game, request.user)
        serializer = GameFavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        url_path='favorites',
        permission_classes=[IsAuthenticated],
    )
    def favorites(self, request):
        favorites = self._interaction_service.list_favorites(request.user)
        serializer = GameFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'patch', 'delete'],
        url_path='library',
        permission_classes=[IsAuthenticated],
    )
    def library(self, request, pk=None):
        game = self._service.get_by_id(pk)

        if request.method == 'DELETE':
            self._interaction_service.remove_library_entry(game, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        entry = self._interaction_service.get_library_entry(game, request.user)
        serializer = GameLibraryEntrySerializer(
            entry,
            data=request.data,
            partial=entry is not None or request.method == 'PATCH',
        )
        serializer.is_valid(raise_exception=True)
        self._interaction_service.save_library_entry(serializer, game, request.user)
        return Response(serializer.data, status=status.HTTP_200_OK if entry else status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['get'],
        url_path='library',
        permission_classes=[IsAuthenticated],
    )
    def my_library(self, request):
        entries = self._interaction_service.list_library(request.user)
        serializer = GameLibraryEntrySerializer(entries, many=True)
        return Response(serializer.data)
