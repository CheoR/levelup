from rest_framework import serializers

from levelupapi.models import Game


class GameSerializer(serializers.ModelSerializer):
    """
        JSON serializer for games.

        Arguments:
            serializer type
    """

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players',
                  'skill_level', 'gametype')
        # depth - Django's version of expand.
        depth = 1
