"""GameTests"""
from levelupapi.models.game import Game
from rest_framework.test import APITestCase
from rest_framework import status

import json

from levelupapi.models import GameType


class GameTests(APITestCase):
    def setUp(self):
        """
            Create  a new account and create sample category.
        """

        url = "/register"
        data = {
            "username": "tacoman",
            "password": "burrito",
            "email": "tacoman@salsa.com",
            "address": "123 Mucho Hot way",
            "phone_number": "555-1212",
            "first_name": "Taco",
            "last_name": "Man",
            "bio": "I <3 tacos"
        }

        # Initialize request and get response
        response = self.client.post(url, data, format="json")

        # Parse JSON response body
        json_response = json.loads(response.content)

        # Since this is a creation POST request, there was no
        # currently assigned token to begin with. Need token later
        # on to make other types of requests for this account.
        # Good time to store auth token
        self.token = json_response["token"]

        # Assert user created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Seed DB with one instance of a GameType
        # This is needed since API  does not expose /gametypes
        # endpoint for creating game types and recreates the DB
        # on every test.
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

    def test_create_game(self):
        """
            Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response['title'], data['title'])
        self.assertEqual(json_response['maker'], data['maker'])
        self.assertEqual(json_response['skill_level'], data['skillLevel'])
        self.assertEqual(
            json_response['number_of_players'], data['numberOfPlayers'])

    def test_get_game(self):
        """
            Ensure we can get an existing game.
        """

        # Seed db
        game = Game()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1

        game.save()

        # authenticate request with user's token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], game.title)
        self.assertEqual(json_response["maker"], game.maker)
        self.assertEqual(json_response["skill_level"], game.skill_level)
        self.assertEqual(
            json_response["number_of_players"], game.number_of_players)

    def test_change_game(self):
        """
            Ensure we can change an existing game.
        """
        game = Game()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        updated_data = {
            "gameTypeId": 1,
            "skillLevel": 2,
            "title": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(
            f"/games/{game.id}", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["maker"], "Hasbro")
        self.assertEqual(json_response["skill_level"], 2)
        self.assertEqual(json_response["number_of_players"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
