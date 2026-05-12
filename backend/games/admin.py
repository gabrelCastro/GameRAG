from django.contrib import admin

from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'platform', 'developer', 'price', 'rating', 'release_date')
    list_filter = ('genre', 'platform')
    search_fields = ('title', 'developer', 'publisher')
    ordering = ('title',)
