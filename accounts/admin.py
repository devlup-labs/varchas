from django.contrib import admin
from .models import UserProfile, CampusAmbassador


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)


class CampusAmbassadorAdmin(admin.ModelAdmin):
    class Meta:
        model = CampusAmbassador


admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)
