import pytest
from django.contrib.auth.models import User
from tournament.models import Tournament, Match, Score
from user.models import Player


@pytest.mark.django_db
def test_tournament_creation():
    tournament = Tournament.objects.create(
        name="Test Tournament", start_date="2024-07-01", end_date="2024-07-10"
    )
    assert tournament.name == "Test Tournament"
    assert tournament.start_date == "2024-07-01"
    assert tournament.end_date == "2024-07-10"


@pytest.mark.django_db
def test_player_creation():
    user = User.objects.create_user(username="testuser", password="password")
    player = Player.objects.create(
        user=user, name="Test Player", age=30, rating=1500, country="USA"
    )
    assert player.name == "Test Player"
    assert player.age == 30
    assert player.rating == 1500
    assert player.country == "USA"


@pytest.mark.django_db
def test_match_creation():
    user1 = User.objects.create_user(username="testuser1", password="password")
    user2 = User.objects.create_user(username="testuser2", password="password")
    player1 = Player.objects.create(
        user=user1, name="Player 1", age=30, rating=1500, country="USA"
    )
    player2 = Player.objects.create(
        user=user2, name="Player 2", age=25, rating=1400, country="CAN"
    )
    tournament = Tournament.objects.create(
        name="Test Tournament", start_date="2024-07-01", end_date="2024-07-10"
    )
    match = Match.objects.create(
        tournament=tournament, player1=player1, player2=player2, round_number=1
    )
    assert match.tournament == tournament
    assert match.player1 == player1
    assert match.player2 == player2
    assert match.round_number == 1
