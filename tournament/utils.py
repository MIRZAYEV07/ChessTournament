from user.models import Player

from .models import Match, Tournament


def generate_swiss_pairings(tournament_id, round_number):
    tournament = Tournament.objects.get(id=tournament_id)
    players = list(tournament.participants.all())
    players.sort(key=lambda player: player.rating, reverse=True)

    pairings = []
    while len(players) > 1:
        player1 = players.pop(0)
        player2 = players.pop(0)
        pairings.append((player1, player2))

    if players:
        player1 = players.pop(0)
        pairings.append((player1, None))

    matches = []
    for player1, player2 in pairings:
        match = Match(
            tournament=tournament,
            player1=player1,
            player2=player2,
            round_number=round_number,
        )
        matches.append(match)

    Match.objects.bulk_create(matches)
    return matches


def calculate_leaderboard(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament)

    # Reset points for all players in the tournament
    for player in tournament.participants.all():
        player.points = 0
        player.save()

    # Calculate points for each player based on match results
    for match in matches:
        if match.winner:
            match.winner.points += 1
            match.winner.save()

    # Retrieve players sorted by points
    players = tournament.participants.all().order_by("-points", "-rating")
    return players
