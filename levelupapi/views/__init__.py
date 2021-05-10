"""Views Module"""
from .auth import register_user
from .auth import login_user

from .gameserializer import GameSerializer
from .gameviewset import GameViewSet

from .gametypeserializer import GameTypeSerializer
from .gametypeviewset import GameTypeViewSet

from .eventserializer import EventSerializer
from .eventviewset import EventViewSet

from .eventgamerserializer import EventGamerSerializer
from .eventuserserializer import EventUserSerializer
