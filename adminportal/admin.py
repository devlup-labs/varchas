from django.contrib import admin
from .models import OurTeam

class ourTeamAdmin(admin.ModelAdmin):
    class Meta:
        model = OurTeam

admin.site.register(OurTeam, ourTeamAdmin)