from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import action
from django.core.cache import cache
from django.db.models import Q
from .models import Match, Tournament, Score
from .serializers import (
    MatchSerializer,
    TournamentSerializer,
    LeaderboardSerializer,
    ScoreSerializer,
)
from .utils import generate_swiss_pairings, calculate_leaderboard
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class TournamentListCreateAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any) -> Response:
        tournaments = cache.get("tournaments")
        if tournaments is None:
            tournaments = Tournament.objects.prefetch_related("participants").all()
            serializer = TournamentSerializer(tournaments, many=True)
            tournaments = serializer.data
            cache.set("tournaments", tournaments, 60 * 5)
        return Response(tournaments)

    def post(self, request: Any) -> Response:
        serializer = TournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("tournaments")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentDetailAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any, pk: int) -> Response:
        cache_key = f"tournament_{pk}"
        tournament = cache.get(cache_key)
        if tournament is None:
            tournament = Tournament.objects.prefetch_related("participants").get(pk=pk)
            serializer = TournamentSerializer(tournament)
            tournament = serializer.data
            cache.set(cache_key, tournament, 60 * 5)
        return Response(tournament)

    def put(self, request: Any, pk: int) -> Response:
        tournament = Tournament.objects.get(pk=pk)
        serializer = TournamentSerializer(tournament, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"tournament_{pk}")
            cache.delete("tournaments")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Any, pk: int) -> Response:
        tournament = Tournament.objects.get(pk=pk)
        tournament.delete()
        cache.delete(f"tournament_{pk}")
        cache.delete("tournaments")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def leaderboard(self, request: Any, pk: Optional[int] = None) -> Response:
        players = calculate_leaderboard(pk)
        serializer = LeaderboardSerializer(players, many=True)
        return Response(serializer.data)


class MatchListCreateAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any) -> Response:
        matches = cache.get("matches")
        if matches is None:
            matches = Match.objects.select_related(
                "tournament", "player1", "player2", "winner"
            ).all()
            serializer = MatchSerializer(matches, many=True)
            matches = serializer.data
            cache.set("matches", matches, 60 * 5)
        return Response(matches)

    def post(self, request: Any) -> Response:
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("matches")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAdminUser]
    )
    def generate_pairings(self, request: Any) -> Response:
        tournament_id = request.data.get("tournament_id")
        round_number = request.data.get("round_number")

        if not tournament_id or not round_number:
            return Response(
                {"error": "tournament_id and round_number are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        matches = generate_swiss_pairings(tournament_id, round_number)
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


class MatchDetailAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any, pk: int) -> Response:
        cache_key = f"match_{pk}"
        match = cache.get(cache_key)
        if match is None:
            match = Match.objects.select_related(
                "tournament", "player1", "player2", "winner"
            ).get(pk=pk)
            serializer = MatchSerializer(match)
            match = serializer.data
            cache.set(cache_key, match, 60 * 5)
        return Response(match)

    def put(self, request: Any, pk: int) -> Response:
        match = Match.objects.get(pk=pk)
        serializer = MatchSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"match_{pk}")
            cache.delete("matches")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Any, pk: int) -> Response:
        match = Match.objects.get(pk=pk)
        match.delete()
        cache.delete(f"match_{pk}")
        cache.delete("matches")
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScoreListCreateAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any) -> Response:
        scores = cache.get("scores")
        if scores is None:
            scores = Score.objects.select_related("player", "tournament").all()
            serializer = ScoreSerializer(scores, many=True)
            scores = serializer.data
            cache.set("scores", scores, 60 * 5)
        return Response(scores)

    def post(self, request: Any) -> Response:
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("scores")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScoreDetailAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request: Any, pk: int) -> Response:
        cache_key = f"score_{pk}"
        score = cache.get(cache_key)
        if score is None:
            score = Score.objects.select_related("player", "tournament").get(pk=pk)
            serializer = ScoreSerializer(score)
            score = serializer.data
            cache.set(cache_key, score, 60 * 5)
        return Response(score)

    def put(self, request: Any, pk: int) -> Response:
        score = Score.objects.get(pk=pk)
        serializer = ScoreSerializer(score, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"score_{pk}")
            cache.delete("scores")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Any, pk: int) -> Response:
        score = Score.objects.get(pk=pk)
        score.delete()
        cache.delete(f"score_{pk}")
        cache.delete("scores")
        return Response(status=status.HTTP_204_NO_CONTENT)
