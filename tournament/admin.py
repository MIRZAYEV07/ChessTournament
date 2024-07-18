from django.contrib import admin

from .models import Tournament, Match, Score


class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("start_date", "end_date")


class MatchAdmin(admin.ModelAdmin):
    list_display = ("tournament", "player1", "player2", "winner", "round_number")
    search_fields = ("tournament__name", "player1__name", "player2__name")
    list_filter = ("tournament", "round_number")


# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ('match', 'player', 'points')
#     search_fields = ('match__tournament__name', 'player__name')
#     list_filter = ('match__tournament',)


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)
# admin.site.register(Score, ScoreAdmin)
