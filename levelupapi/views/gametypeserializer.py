from rest_framework import serializers

from levelupapi.models import GameType


class GameTypeSerializer(serializers.ModelSerializer):
    """
        JSON Game type serializer.

        Aguments:
            serializers
    """

    class Meta:
        model = GameType
        fields = ('id', 'label')
