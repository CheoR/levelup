from rest_framework import serializers


from levelupapi.views.eventgamerserializer import EventGamerSerializer
from levelupapi.views.gameserializer import GameSerializer
from levelupapi.models import Event


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    # Note you can nest serializers.
    organizer = EventGamerSerializer(many=False)

    # If the field is used to represent a to-many relationship,
    #  you should add the many=True flag to the serializer field.
    # Embedded serializer is good so you only get fields you want
    # instead of getting all fields when using
    # depth = 1
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
                  'description', 'start_date', 'description', 'joined')
