"""EventTests"""

from rest_framework import status
from rest_framework.test import APITestCase

import json

from levelupapi.models import Event, Game, GameType


class EventTests(APITestCase):
    def setUp(self):
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        # Cannot assign token before user is created and returned with a token.
        self.token = json_response["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.gametype = GameType()
        self.gametype.name = "Board game"
        self.gametype.save()

        self.game = Game()
        self.game.gametype_id = 1
        self.game.skill_level = 5
        self.game.name = "Clue"
        self.game.maker = "Milton Bradley"
        self.game.num_of_players = "6"
        self.game.gamer_id = 1

        self.game.save()

        self.event = Event()
        self.event.time = "06:30:00"
        self.event.event_date = "2021-05-20T00:00:00Z"
        self.event.description = "Seeded Game"
        self.event.game_id = 1
        self.event.organizer_id = 1

        self.event.save()

        self.data = {
            "time": "15:30:00",
            "eventDate": "2021-05-20T00:00:00Z",
            "description": "description",
            "gameId": 1
        }

    def test_create_event(self):
        response = self.client.post(f"/events", self.data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["time"], self.data["time"])
        self.assertEqual(json_response["event_date"], self.data["eventDate"])
        self.assertEqual(
            json_response["description"], self.data["description"])

    def test_get_event(self):
        response = self.client.get(f"/events/{self.event.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["time"], self.event.time)
        self.assertEqual(json_response["event_date"], self.event.event_date)
        self.assertEqual(json_response["description"], self.event.description)

    def test_update_event(self):
        response = self.client.put(
            f"/events/{self.event.id}", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/events/{self.event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(json_response["time"], self.data["time"])
        self.assertEqual(json_response["event_date"], self.data["eventDate"])
        self.assertEqual(
            json_response["description"], self.data["description"])

    def test_destroy_event(self):
        response = self.client.delete(f"/events/{self.event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/events/{self.event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
