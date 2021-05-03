from django.db import models

# from .game import Game
from .gamer import Gamer


class Event(models.Model):
    """
        Event model.
        To define a many-to-one relationship, use ForeignKey

        "Game" - alternative way to refer to model without having to import it.
    """

    event_date = models.DateField()
    description = models.CharField(max_length=100)
    organizer_id = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
