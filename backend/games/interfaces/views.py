from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from games.application.game_service import GameService
from games.application.recommendation_service import RecommendationService
from games.interfaces.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'genre', 'platform', 'developer', 'publisher']
    ordering_fields = ['title', 'price', 'rating', 'release_date']
    ordering = ['title']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = GameService()
        self._recommendation_service = RecommendationService()

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
