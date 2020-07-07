from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import HomeImageCarousel, NavBarSubOptions, HomeEventCard, HomeBriefCard
from django.shortcuts import get_object_or_404, render
from accounts.models import UserProfile
from rest_framework import viewsets
from adminportal.models import OurTeam
from .serializers import OurTeamSerializer
from rest_framework import permissions


class OurTeamView(TemplateView):
    template_name = 'main/our_team.html'
    model = OurTeam

    def get_context_data(self, **kwargs):
        context = super(OurTeamView, self).get_context_data(**kwargs)
        context["our_team"] = OurTeam.objects.all
        context['page'] = "ourTeam"
        return context


class OurTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OurTeam.objects.all()
    serializer_class = OurTeamSerializer
    permission_classes = [permissions.IsAdminUser]


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        if self.request.user.username != "":
            userprofile = get_object_or_404(
                UserProfile, user=self.request.user)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['carousel'] = HomeImageCarousel.objects.filter(
            active=True).order_by('ordering')
        context['event_list'] = HomeEventCard.objects.all
        context['brief_list'] = HomeBriefCard.objects.all
        if self.request.user.username != "":
            context['userprofile'] = userprofile
            context['page'] = "home"
        return context


class NavBarSubOptionsPageView(DetailView):
    template_name = 'main/navbarsuboptionpage.html'
    model = NavBarSubOptions

    def get_context_data(self, **kwargs):
        context = super(NavBarSubOptionsPageView, self).get_context_data()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object.use_custom_html:
            self.template_name = self.object.custom_html
        else:
            self.template_name = 'main/navbarsuboptionpage.html'
        return self.render_to_response(context)


def comingSoon(request):
    return render(request, 'main/comingSoon.html')


def error_404(request, exception):
    return render(request, 'main/error_404.html', status=404)


def error_500(request):
    return render(request, 'main/error_500.html', status=500)
