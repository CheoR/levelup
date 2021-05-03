from django.db import models

from .game_type import GameType


class Game(models.Model):
    """
        Game model.
    """
    name = models.CharField(max_length=50)
    difficulty = models.IntegerField()
    players = models.IntegerField()

    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
