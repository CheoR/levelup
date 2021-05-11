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
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    description = models.TextField()

    attendees = models.ManyToManyField(
        "Gamer",
        # Django will automatically generate a table to manage
        #  many-to-many relationships. However, if you want to manually
        #  specify the intermediary table, you can use the through
        #  option to specify the Django model that represents the
        #  intermediate table that you want to use.
        # The most common use for this option is when you want to
        #  associate extra data with a many-to-many relationship.
        through="EventAttendee",
        # The name to use for the relation from the related object back to this one.
        related_name="attending")
