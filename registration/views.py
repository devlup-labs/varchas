from django.views.generic import CreateView
from .forms import CampusAmbassadorForm, TeamRegistrationForm, TeamRegistrationForm1, RemovePlayerForm
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from django.http import HttpResponse
from random import random
from .models import Team
from django.core.mail import send_mail
from django.views.generic import FormView
from django.contrib.auth.models import User


class CampusAmbassadorRegisterView(CreateView):
    template_name = 'registration/ca_reg.html'
    success_url = '/'
    form_class = CampusAmbassadorForm


class TeamFormationView(CreateView):
    form_class = TeamRegistrationForm
    template_name = 'registration/team.html'
    success_url = '/account/myTeam'

    def form_valid(self, form):
        user = self.request.user
        if user is not None:
            data = self.request.POST.copy()
            spor = Team.SPORT_CHOICES[int(data['sport'])-1][1][:3]
            data['teamId'] = "VA-" + spor[:3].upper() + '-' + user.username[:3].upper() + "{}".format(int(random()*100))
            form = TeamRegistrationForm1(data)
            user = get_object_or_404(UserProfile, user=user)
            if user.teamId != "NULL":
                message = "You are already in team {}".format(user.teamId)
                message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                return HttpResponse(message, content_type="text/plain")
            team = form.save()
            team.captian = user
            user.teamId = team.teamId
            user.save()
            team.members.add(user)

            message = '''<!DOCTYPE html> <html><body>Hi {}!<br>You have successfully registered for Varchas2020.<br>Your teamId is: <b>{}</b><br>
                          Check your team details here: <a href="http://varchas2020.org/account/myTeam">varchas2020.org/accou
                          nt/myTeam</a><p>Get Your Game On.</p></body></html>'''.format(user.user.first_name, user.teamId)
            send_mail('Varchas Team Created', message, 'noreply@varchas2020.org', [team.captian.user.email],
                      fail_silently=False, html_message=message)

            return super(TeamFormationView, self).form_valid(form)
        return HttpResponse("404")


# @login_required(login_url="login")
class removePlayerView(FormView):
    form_class = RemovePlayerForm
    template_name = 'registration/remove_player.html'
    success_url = '/account/myTeam'

    def form_valid(self, form):
        user = get_object_or_404(UserProfile, user=self.request.user)
        if user.teamId == "NULL":
            return HttpResponse("You must registered in a team to complete this operation.")
        team = get_object_or_404(Team, captian=user)
        user = get_object_or_404(User, email=form['player'].value())
        user = get_object_or_404(UserProfile, user=user)
        user.teamId = "NULL"
        user.save()
        team.members.remove(user)
        return super(removePlayerView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(removePlayerView, self).get_context_data(**kwargs)
        user = get_object_or_404(UserProfile, user=self.request.user)
        team = get_object_or_404(Team, captian=user)
        context['players'] = team.members.all()
        return context
