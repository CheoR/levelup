from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from levelupapi.models import GameType
from .gametypeserializer import GameTypeSerializer

"""
    View module for handling requests about game types.
"""


class GameTypeViewSet(ViewSet):
    """
        Levelup game type viewset.
    """

    def retrieve(self, request, pk=None):
        """
            Handle GET requests for single game type.
            Returns:
                Response : JSON serialized game type.
        """

        try:
            game_type_obj = GameType.objects.get(pk=pk)
            serialized_game_type = GameTypeSerializer(
                game_type_obj,
                context={'request': request})

            return Response(serialized_game_type.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
            Handle GET requests to get all game types.
            Returns:
                Response : JSON serialized list of game types.
        """

        game_type_objects = GameType.objects.all()

        # Note additonal 'many=True'
        # It's for serializing a list of objects instead of one.
        serialized_game_types = GameTypeSerializer(
            game_type_objects,
            many=True,
            context={'request': request}
        )

        return Response(serialized_game_types.data)
