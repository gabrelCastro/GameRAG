from django.contrib import admin

from games.models import Game, GameFavorite, GameLibraryEntry, GameReview


class GameReviewInline(admin.TabularInline):
    model = GameReview
    extra = 1
    fields = ('user', 'rating', 'comment')


class GameFavoriteInline(admin.TabularInline):
    model = GameFavorite
    extra = 0
    fields = ('user', 'created_at')
    readonly_fields = ('created_at',)


class GameLibraryEntryInline(admin.TabularInline):
    model = GameLibraryEntry
    extra = 0
    fields = ('user', 'status', 'hours_played', 'updated_at')
    readonly_fields = ('updated_at',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'platform', 'developer', 'price', 'rating', 'release_date')
    list_filter = ('genre', 'platform')
    search_fields = ('title', 'developer', 'publisher')
    ordering = ('title',)
    inlines = [GameReviewInline, GameFavoriteInline, GameLibraryEntryInline]


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('game__title', 'user__username')


@admin.register(GameFavorite)
class GameFavoriteAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'created_at')
    search_fields = ('game__title', 'user__username')


@admin.register(GameLibraryEntry)
class GameLibraryEntryAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'status', 'hours_played', 'updated_at')
    list_filter = ('status',)
    search_fields = ('game__title', 'user__username')
