"""Views Module"""
from .auth import login_user
from .auth import register_user

from .gameviewset import GameViewSet
from .gameserializer import GameSerializer

from .gametypeviewset import GameTypeViewSet
from .gametypeserializer import GameTypeSerializer

from .eventviewset import EventViewSet
from .eventserializer import EventSerializer
