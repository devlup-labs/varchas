from django.contrib import admin
from .models import CampusAmbassador, Team


class CampusAmbassadorAdmin(admin.ModelAdmin):
    class Meta:
        model = CampusAmbassador


admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)


class TeamAdmin(admin.ModelAdmin):
    class Meta:
        model = Team


admin.site.register(Team, TeamAdmin)
