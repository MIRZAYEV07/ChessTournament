from django.urls import path
from .views import PlayerListCreateAPIView, PlayerDetailAPIView

urlpatterns = [
    path("players/", PlayerListCreateAPIView.as_view(), name="player-list-create"),
    path("players/<int:pk>/", PlayerDetailAPIView.as_view(), name="player-detail"),
]
