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

    def __str__(self):
        return f'{self.user} → {self.game} ({self.rating}/10)'
