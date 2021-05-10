"""View module for handling events requests"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from levelupapi.views.eventserializer import EventSerializer
from levelupapi.views.gameserializer import GameSerializer
from levelupapi.models import Game, Event, Gamer


class EventViewSet(ViewSet):
    """
        Event ViewSet.
    """

    def create(self, request):
        """
            Handle POST requests for events.

            Returns:
                Response -- JSON serialized even instance.
        """

        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['gameId'])

        event = Event()
        event.description = request.data['description']
        event.time = request.data['time']
        event.date = request.data['date']
        event.organizer = gamer
        event.game = game

        try:
            event.save()
            serialized_event = EventSerializer(
                event, context={'request': request})
            return Response(serialized_event.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
            Handle GET requests for single event.
        """

        try:
            event = Event.objects.get(pk=pk)
            serialized_event = EventSerializer(
                event, context={'request': request})
            return Response(serialized_event.data)
        except Exception:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """
            Handle DELETE requests for a single game.

            Returns:
                Response -- 200, 204, 500 status code.
        """

        try:
            event = Event.objects.get(pk=pk)
            event.date()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
            Handle GET requests to events resource

            Returns:
                Response -- JSON serialized list of events
        """
        events = Event.objects.all()

        # Support filtering events by game
        game = self.request.query_params.get('gameId', None)

        if game is not None:
            # note double underscore
            # acts as SQL join
            events = events.filter(game__id=game)

        serialized_event = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serialized_event.data)
