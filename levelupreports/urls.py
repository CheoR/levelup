from django.urls import path
from .views import usergame_list, userevent_list

urlpatterns = [
    # where the first slot is the endpoint
    # and the second is the function that will handle the
    # request when client hits that endpoint
    path('reports/usergames', usergame_list),
    path('reports/userevents', userevent_list),
]
