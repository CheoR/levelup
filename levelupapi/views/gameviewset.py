from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status

from levelupapi.models import Game, GameType, Gamer
from .gametypeserializer import GameTypeSerializer
from .gameserializer import GameSerializer

"""
    View module for handling requests about game types.
    ViewSet handles GET, POST, PUT, DELETE requests sent from client
    over HTTP protocol.
"""


class GameViewSet(ViewSet):
    """
        Levelup game type viewset.
    """

    def create(self, request):
        """
            Handle POST requests.

            Returns:
                Response -- serialized JSON game instance.
        """

        # Use Token passed in the 'Authorization' header
        # Where user is a property on Gamer class.
        gamer = Gamer.objects(user=request.auth.user)

        # Create a new Python instance of the Game class.
        # Use data from the request argument to fill in the
        # properties of the Game instance.
        game = Game()
        game.title = request.data['title']
        game.make = request.data['maker']
        game.number_of_players = request.data['number_of_players']
        game.skill_level = request.data['skillLevel']
        game.gamer = gamer

        # Use Django's ORM to fetch record that matches passed-in
        # gameTypeId in the request from the db.
        gametype = GameType.objects.get(pk=request.data['gameTypeId'])
        game.gametype = gametype

        # Try to save the new game instance to db.
        # If valid, serialize and return the instance as JSON object
        # and return to client in a Response objct
        try:
            game.save()
            serialized_game = GameTypeSerializer(
                game, context={'request': request})

            return Response(serialized_game.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def retrieve(self, request, pk=None):
        """
            Handle GET requests for single game.

            Returns:
                Response : JSON serialized game.
        """

        try:
            # 'pk' - parameter to function
            # Django parses it from the URL
            # http://localhost:8000/games/2
            # '2' - becomes pk
            game__obj = Game.objects.get(pk=pk)
            serialized_game = GameSerializer(
                game__obj,
                context={'request': request})

            return Response(serialized_game.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
            Handle PUT request for a game.

            Returns:
                Response -- Empty body with 204 status code.
        """

        gamer = Gamer.objects.get(user=request.user.auth)

        # Simlar to POST.
        # Instead of creating new instance, update exisiting record.
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer

        gametype = GameType.objects.get(pk=request.data['gameTypeId'])
        game.gametype = gametype
        game.save()

        # 204 - everything worked but server has nothing to send back
        # in response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
            Handle DELETE requests for single game.

            Returns:
                Response -- 200, 404 or 500
        """

        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
            Handle GET requests to get all game resources.

            Returns:
                Response : JSON serialized list of game types.
        """

        game_objects = Game.objects.all()

        # filter games by type
        # http://localhost:8000/games?type=1
        # 1 - tabletop games
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            # Note: there are two  underscores between gametype and
            # id. They denote a query join.
            game_objects = game_objects.fiter(gametype__id=game_type)

        # Note additonal 'many=True'
        # It's for serializing a list of objects instead of one.
        serialized_games = GameSerializer(
            game_objects,
            many=True,
            context={'request': request}
        )

        return Response(serialized_games.data)
