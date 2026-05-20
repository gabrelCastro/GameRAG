from rest_framework import serializers

from games.models import Game, GameFavorite, GameLibraryEntry, GameReview


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id',
            'title',
            'description',
            'genre',
            'platform',
            'price',
            'developer',
            'publisher',
            'release_date',
            'tags',
            'rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Rating deve ser entre 0 e 10.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Preço não pode ser negativo.')
        return value

    def validate_tags(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Tags deve ser uma lista.')
        if not all(isinstance(tag, str) for tag in value):
            raise serializers.ValidationError('Cada tag deve ser uma string.')
        return value


class GameReviewSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = GameReview
        fields = ['id', 'game', 'user', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'game', 'user', 'username', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError('Rating deve ser entre 1 e 10.')
        return value


class GameFavoriteSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = GameFavorite
        fields = ['id', 'game', 'created_at']
        read_only_fields = ['id', 'game', 'created_at']


class GameLibraryEntrySerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)

    class Meta:
        model = GameLibraryEntry
        fields = ['id', 'game', 'status', 'hours_played', 'created_at', 'updated_at']
        read_only_fields = ['id', 'game', 'created_at', 'updated_at']

    def validate_hours_played(self, value):
        if value < 0:
            raise serializers.ValidationError('Horas jogadas não pode ser negativo.')
        return value
