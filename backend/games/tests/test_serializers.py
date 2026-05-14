from django.test import SimpleTestCase

from games.interfaces.serializers import GameSerializer


class GameSerializerTests(SimpleTestCase):
    def _valid_payload(self, **overrides):
        payload = {
            'title': 'The Witcher 3',
            'description': 'RPG de mundo aberto.',
            'genre': 'RPG',
            'platform': 'PC',
            'price': '99.90',
            'developer': 'CD Projekt Red',
            'publisher': 'CD Projekt',
            'release_date': '2015-05-19',
            'tags': ['RPG', 'Open World'],
            'rating': '9.8',
        }
        payload.update(overrides)
        return payload

    def test_valid_payload_is_accepted(self):
        serializer = GameSerializer(data=self._valid_payload())

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_accepts_boundary_values_for_price_rating_and_tags(self):
        serializer = GameSerializer(data=self._valid_payload(price='0.00', rating='10.0', tags=[]))

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_embedding_is_not_exposed_to_api_clients(self):
        serializer = GameSerializer()

        self.assertNotIn('embedding', serializer.fields)

    def test_rejects_negative_price(self):
        serializer = GameSerializer(data=self._valid_payload(price='-1.00'))

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_rejects_negative_rating(self):
        serializer = GameSerializer(data=self._valid_payload(rating='-0.1'))

        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)

    def test_rejects_rating_greater_than_ten(self):
        serializer = GameSerializer(data=self._valid_payload(rating='10.1'))

        self.assertFalse(serializer.is_valid())
        self.assertIn('rating', serializer.errors)

    def test_rejects_tags_that_are_not_a_list(self):
        serializer = GameSerializer(data=self._valid_payload(tags='RPG'))

        self.assertFalse(serializer.is_valid())
        self.assertIn('tags', serializer.errors)

    def test_rejects_tags_that_are_not_strings(self):
        serializer = GameSerializer(data=self._valid_payload(tags=['RPG', 123]))

        self.assertFalse(serializer.is_valid())
        self.assertIn('tags', serializer.errors)

    def test_ignores_read_only_fields_from_input(self):
        serializer = GameSerializer(
            data=self._valid_payload(
                id=999,
                created_at='2026-01-01T00:00:00Z',
                updated_at='2026-01-01T00:00:00Z',
            )
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('id', serializer.validated_data)
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertNotIn('updated_at', serializer.validated_data)
