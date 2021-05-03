from django.db import models


class EventAttendee(models.Model):
    """
        EventAttendee model.
    """

    event_id = models.ForeignKey("Event", on_delete=models.CASCADE)
    gamer_id = models.ForeignKey("Gamer", on_delete=models.CASCADE)
