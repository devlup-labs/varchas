from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import NavBarSubOptions, OurTeam, HomeEventCard
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from accounts.models import UserProfile
from rest_framework import viewsets
from .serializers import OurTeamSerializer
from rest_framework import permissions


class IndexView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            if UserProfile.objects.filter(user=user):
                userprofile = get_object_or_404(UserProfile, user=user)
            else:
                logout(self.request)
        context = super(IndexView, self).get_context_data(**kwargs)
        context['event_list'] = HomeEventCard.objects.all
        if User.objects.filter(username=user.username):
            if UserProfile.objects.filter(user=user):
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


class OurTeamView(TemplateView):
    template_name = 'main/our_team.html'
    model = OurTeam

    def get_context_data(self, **kwargs):
        context = super(OurTeamView, self).get_context_data(**kwargs)
        context["our_team"] = OurTeam.objects.all
        context['page'] = "ourTeam"
        return context


def comingSoon(request):
    return render(request, 'main/comingSoon.html')


def error_404(request, exception):
    return render(request, 'main/error_404.html', status=404)


def error_500(request):
    return render(request, 'main/error_500.html', status=500)


class OurTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OurTeam.objects.all()
    serializer_class = OurTeamSerializer
    permission_classes = [permissions.IsAdminUser]
