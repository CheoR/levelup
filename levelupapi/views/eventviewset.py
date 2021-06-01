"""View module for handling events requests"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from levelupapi.views.eventserializer import EventSerializer
from levelupapi.models import Game, Event, Gamer, EventAttendee


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
        event.start_date = request.data['start_date']
        event.organizer = gamer
        event.game = game

        try:
            event.save()
            serialized_event = EventSerializer(
                event, context={'request': request})
            return Response(serialized_event.data, status=status.HTTP_201_CREATED)
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
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """
            Handle DELETE requests for a single game.

            Returns:
                Response -- 200, 204, 500 status code.
        """

        try:
            event = Event.objects.get(pk=pk)
            event.delete()

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
        # Current authenticated user
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.all()

        # set 'joined' property on every event
        for event in events:
            # check to see if the gamer is in the attendees
            # list on the event
            event.joined = gamer in event.attendees.all()

        # Support filtering events by game
        # Can take out self, just a differnt way of looking at request.
        game = self.request.query_params.get('gameId', None)

        if game is not None:
            # note double underscore
            # acts as SQL join
            events = events.filter(game__id=game)

        serialized_event = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serialized_event.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = organizer

        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """
            Manage users signup to event.
        """

        # Confirm which user is making the request to sign up
        # with Djagno's 'Authoriizatin' header
        gamer = Gamer.objects.get(user=request.auth.user)

        # when event does not exist
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'message': 'Event does not exist.'},
                satus=status.HTTP_400_BAD_REQUEST
            )

        # sign up action
        if request.method == "POST":
            try:
                event.attendees.add(gamer)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == "DELETE":
            try:
                event.attendees.remove(gamer)
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #     # pk is event id user wants to sign up for
        #     event = Event.objects.get(pk=pk)

        #     try:
        #         # is user already signed up
        #         isRegistered = EventAttendee.objects.get(
        #             event=event,
        #             gamer=gamer)
        #         return Response(
        #             {'message': 'Gamer already signed up.'},
        #             status=status.HTTP_422_UNPROCESSABLE_ENTITY
        #         )
        #     except EventAttendee.DoesNotExist:
        #         isRegistered = EventAttendee()
        #         isRegistered.event = event
        #         isRegistered.gamer = gamer
        #         isRegistered.save()

        #         return Response({}, status=status.HTTP_201_CREATED)
        # # Leave previously joined event
        # elif request.method == "DELETE":
        #     # when an event does not exist
        #     # get authenticated user
        #     gamer = Gamer.objects.get(user=request.auth.user)

        #     try:
        #         # try delete from signup
        #         isRegistered = EventAttendee.objects.get(
        #             event=event,
        #             gamer=gamer
        #         )
        #         isRegistered.delete()

        #         return Response(None, status=status.HTTP_204_NO_CONTENT)

        #     except EventAttendee.DoesNotExist:
        #         return Response(
        #             {'message': 'Not registered for event.'},
        #             status=status.HTTP_404_NOT_FOUND
        #         )
        # # Advise client any method other than POST, DELETE not supported
        # return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
