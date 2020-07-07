from adminportal.models import OurTeam
from rest_framework import serializers


class OurTeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OurTeam
        fields = ['name', 'position', 'phone', 'email', ]
