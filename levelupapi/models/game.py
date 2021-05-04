from django.db import models

from .gametype import GameType


class Game(models.Model):
    """
        Game model.
    """
    name = models.CharField(max_length=50)
    difficulty = models.IntegerField()
    players = models.IntegerField()

    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, default=None)
    game_type = models.ForeignKey(GameType, on_delete=models.CASCADE)
