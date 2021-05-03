from django.db import models


class Event(models.Model):
    """
        Event model.
        To define a many-to-one relationship, use ForeignKey
    """
    pass
    # event_date = models.DateField()
    # game_id = models.ForeignKey(, on_delete=models.CASCADE)
    # organizer_id = models.ManyToOneRel
    # description = models.CharField(max_length=100)
