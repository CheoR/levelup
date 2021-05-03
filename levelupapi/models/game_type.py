from django.db import models


class GameType(models.Model):
    """
        GameType model.
    """
    type = models.CharField(max_length=50)
