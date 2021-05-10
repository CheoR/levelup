from django.db import models

# from .game import Game
from .gamer import Gamer


class Event(models.Model):
    """
        Event model.
        To define a many-to-one relationship, use ForeignKey

        "Game" - alternative way to refer to model without having to import it.
    """

    # Changing DateField to DateTimeField allows you to add hour time in fixtures.
    date = models.DateTimeField()
    time = models.TimeField(auto_now=True)
    description = models.CharField(max_length=100)
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
