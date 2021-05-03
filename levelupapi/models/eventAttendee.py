from django.db import models


class EventAttendee(models.Model):
    """
        EventAttendee model.
    """

    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
