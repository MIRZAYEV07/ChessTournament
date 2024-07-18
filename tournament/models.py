from django.db import models
from user.models import Player


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(
        Player, related_name="tournaments", blank=True
    )

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player1 = models.ForeignKey(
        Player, related_name="player1", on_delete=models.CASCADE
    )
    player2 = models.ForeignKey(
        Player, related_name="player2", on_delete=models.CASCADE
    )
    winner = models.ForeignKey(
        Player, related_name="winner", on_delete=models.CASCADE, null=True, blank=True
    )
    round_number = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.player1} vs {self.player2} - Round {self.round_number}"


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.player} - {self.points} points in {self.tournament}"
