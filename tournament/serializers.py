from rest_framework import serializers
from user.models import Player
from .models import Tournament, Match, Score


class TournamentSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), many=True
    )

    class Meta:
        model = Tournament
        fields = ["id", "name", "start_date", "end_date", "participants"]


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["id", "tournament", "player1", "player2", "winner", "round_number"]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "rating", "points", "country"]
