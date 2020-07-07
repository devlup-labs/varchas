from django.urls import path
from .views import IndexView, NavBarSubOptionsPageView, comingSoon, OurTeamView, OurTeamViewSet
from django.conf.urls import url, include
from rest_framework import routers

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'team', OurTeamViewSet)

urlpatterns = [
    url(r'^comingSoon$', comingSoon, name='comingSoon'),
    path('', IndexView.as_view(), name='home'),
    path('OurTeam', OurTeamView.as_view(), name='OurTeam'),
    path('<slug:slug>', NavBarSubOptionsPageView.as_view(),
         name='navbarsuboptionpage'),
    path('mainapi/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
