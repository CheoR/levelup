from rest_framework import serializers

from levelupapi.views.eventuserserializer import EventUserSerializer
from levelupapi.models import Gamer


class EventGamerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']
