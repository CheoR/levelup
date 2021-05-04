from django.db import models


class GameType(models.Model):
    """
        GameType model.
    """
    label = models.CharField(max_length=50)
