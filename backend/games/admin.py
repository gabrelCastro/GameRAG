from django.contrib import admin

from games.models import Game, GameReview


class GameReviewInline(admin.TabularInline):
    model = GameReview
    extra = 1
    fields = ('user', 'rating', 'comment')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'platform', 'developer', 'price', 'rating', 'release_date')
    list_filter = ('genre', 'platform')
    search_fields = ('title', 'developer', 'publisher')
    ordering = ('title',)
    inlines = [GameReviewInline]


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('game__title', 'user__username')
