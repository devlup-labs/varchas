from .views import CampusAmbassadorRegisterView, TeamFormationView, removePlayerView
from django.urls import path
from django.conf.urls import url


app_name = 'teams'

urlpatterns = [
    path('ca', CampusAmbassadorRegisterView.as_view(), name='ca'),
    path('team', TeamFormationView.as_view(), name='team'),
    url(r'removePlayer$', removePlayerView.as_view(), name='remove_player'),
    # url(r'team/(?P<username>[a-zA-Z0-9]+)$',TeamFormationView),
]
