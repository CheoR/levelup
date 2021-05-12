"""Profile ViewSet"""
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers

from levelupapi.models import Gamer, Event, Game


class ProfileViewSet(ViewSet):
    """
        Gamer can see profile information when hittinging
            /profiles
        end point without having to pass explicit gamer id since
        it is fetched from the Authorization token.
    """

    def list(self, request):
        """
            Handle GET requests to profile resource.

            Returns:
                Response -- JSON representation of user info and events.
        """

        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(attendees=gamer)

        # serializers will stay in this file since they differ from
        # other serializers with the same name, but differ what to
        # return
        events = EventSerializer(
            events, many=True, context={'request': request})

        # note many=False, this is because we are only expecting one object back
        # not a list/query set
        gamer = GamerSerializer(
            gamer, many=False, context={'request': request})

        # Manually construct JSON structure you want in the response.
        # Note: Response will serialize profile dictionary
        profile = {}
        profile["gamer"] = gamer.data
        profile["events"] = events.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('title',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time')
