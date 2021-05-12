"""Profile ViewSet"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from levelupapi.models import Gamer, Event


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
