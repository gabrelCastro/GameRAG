from rest_framework import serializers

from games.models import Game


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
