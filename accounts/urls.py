from .views import RegisterView, DisplayProfile, joinTeam, DisplayTeam, leaveTeam, UserViewSet, GroupViewSet, GoogleCreateProfileView
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', RegisterView.as_view(), name='register'),
    path('googleregister/', GoogleCreateProfileView.as_view(), name='google-register'),
    url(r'profile$', DisplayProfile, name='profile'),
    url(r'^myTeam$', DisplayTeam, name='myTeam'),
    url(r'joinTeam$', joinTeam, name='joinTeam'),
    url(r'^leaveTeam$', leaveTeam, name='leaveTeam'),

]
