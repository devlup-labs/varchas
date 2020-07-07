from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    class Meta:
        model = Team


admin.site.register(Team, TeamAdmin)
