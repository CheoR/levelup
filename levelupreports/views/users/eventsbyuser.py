"""Module for generating events by user report."""
from django.shortcuts import render
import sqlite3

from levelupapi.models import EventAttendee
from levelupapi.models import Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function builds an HTML report of events user is attending."""

    if request.method == "GET":
        with sqlite3.connect(Connection.absolute_path_to_db) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT gr.id AS gamer_id,
                    u.first_name || ' ' || u.last_name AS full_name,
                    e.id AS event_id,
                    e.start_date,
                    g.title
                FROM levelupapi_event e
                JOIN levelupapi_gamer gr
                    ON e.organizer_id = gr.id
                JOIN auth_user u 
                    ON u.id = gr.user_id
                JOIN levelupapi_game g ON
                    g.id = e.game_id
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "organizer_id": 1,
            #         "full_name": "Admina Straytor",
            #         "events": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "start_date": "2021-10-04 00:00:00"
            #             }
            #         ]
            #     }
            # }

            events_by_user = {}

            for row in dataset:

                event = {
                    "id": row['event_id'],
                    "start_date": row['start_date'],
                    "game_event": row['title']
                }

                uid = row['gamer_id']

                # if gamer id alraedy a dictionary key
                if uid in events_by_user:
                    events_by_user[uid]['events'].append(event)
                else:
                    events_by_user[uid] = {
                        'organizer_id': uid,
                        'full_name': row['full_name'],
                        'events': [event]
                    }

            list_of_attendees = sorted(list(events_by_user.values()))

            template = 'users/list_with_events.html'
            context = {
                'event_host_list': list_of_attendees,
                'title': 'List of users hosted events'
            }

            return render(request, template, context)
