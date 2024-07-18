from django.urls import path
from .views import (
    TournamentListCreateAPIView,
    TournamentDetailAPIView,
    MatchListCreateAPIView,
    MatchDetailAPIView,
    ScoreListCreateAPIView,
    ScoreDetailAPIView,
)

urlpatterns = [
    path(
        "tournaments/",
        TournamentListCreateAPIView.as_view(),
        name="tournament-list-create",
    ),
    path(
        "tournaments/<int:pk>/",
        TournamentDetailAPIView.as_view(),
        name="tournament-detail",
    ),
    path("matches/", MatchListCreateAPIView.as_view(), name="match-list-create"),
    path("matches/<int:pk>/", MatchDetailAPIView.as_view(), name="match-detail"),
    path("scores/", ScoreListCreateAPIView.as_view(), name="score-list-create"),
    path("scores/<int:pk>/", ScoreDetailAPIView.as_view(), name="score-detail"),
]
