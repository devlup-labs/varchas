from django.contrib import admin
from .models import HomeImageCarousel, NavBarOptions, NavBarSubOptions, HomeEventCard, HomeBriefCard


class HomeImageCarouselAdmin(admin.ModelAdmin):
    class Meta:
        model = HomeImageCarousel


admin.site.register(HomeImageCarousel, HomeImageCarouselAdmin)


@admin.register(NavBarOptions)
class NavBarOptionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active', ]
    search_fields = ['title', ]

    class Meta:
        model = NavBarOptions
        fields = '__all__'


@admin.register(NavBarSubOptions)
class NavBarSubOptionsAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    search_fields = ['title', ]

    class Meta:
        model = NavBarSubOptions
        fields = '__all__'


admin.site.register(HomeEventCard)

admin.site.register(HomeBriefCard)
