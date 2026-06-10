from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from pgvector.django import VectorField


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    genre = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    release_date = models.DateField()
    tags = models.JSONField(default=list, blank=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    # text-embedding-3-small da OpenAI gera vetores de 1536 dimensões
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'

    def __str__(self):
        return f'{self.title} ({self.platform})'


class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('game', 'user')
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f'{self.user} → {self.game} ({self.rating}/10)'


class GameFavorite(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('game', 'user')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f'{self.user} favoritou {self.game}'


class GameLibraryEntry(models.Model):
    STATUS_WANT_TO_PLAY = 'want_to_play'
    STATUS_PLAYING = 'playing'
    STATUS_COMPLETED = 'completed'
    STATUS_DROPPED = 'dropped'

    STATUS_CHOICES = [
        (STATUS_WANT_TO_PLAY, 'Quero jogar'),
        (STATUS_PLAYING, 'Jogando'),
        (STATUS_COMPLETED, 'Concluído'),
        (STATUS_DROPPED, 'Abandonado'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='library_entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_library')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_WANT_TO_PLAY)
    hours_played = models.DecimalField(
        max_digits=7,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('game', 'user')
        verbose_name = 'Entrada de Biblioteca'
        verbose_name_plural = 'Entradas de Biblioteca'

    def __str__(self):
        return f'{self.user} - {self.game} ({self.status})'
