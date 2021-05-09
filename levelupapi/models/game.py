from django.db import models

from .gametype import GameType


class Game(models.Model):
    """
        Game model.
    """
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    skill_level = models.IntegerField()
    number_of_players = models.IntegerField()

    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE, default=None)
    gametype = models.ForeignKey(GameType, on_delete=models.CASCADE)
