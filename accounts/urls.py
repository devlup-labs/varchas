from . import views
from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('createprofile/', views.CreateUserProfileView.as_view(), name='createprofile'),
    url(r'profile$', views.DisplayProfile, name='profile'),
    url(r'^myTeam$', views.DisplayTeam, name='myTeam'),
    url(r'joinTeam$', views.joinTeam, name='joinTeam'),
    url(r'^leaveTeam$', views.leaveTeam, name='leaveTeam'),

]
