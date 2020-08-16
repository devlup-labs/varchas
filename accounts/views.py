from django.views.generic import CreateView
from .models import UserProfile
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from registration.models import TeamRegistration
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = RegisterForm(data)
        user = form.save()
        RegisterView.create_profile(user, **form.cleaned_data)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = UserProfile.objects.create(user=user, gender=kwargs['gender'], phone=kwargs['phone'],
                                                 college=kwargs['college'],
                                                 state=kwargs['state'],
                                                 accommodation_required=kwargs['accommodation_required'],
                                                 referral=kwargs['referred_by']
                                                 )
        userprofile.save()


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('adminportal:dashboard')
        else:
            return reverse('main:home')


@login_required(login_url="login")
def DisplayProfile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'accounts/profile.html', {'userprofile': user, 'user': request.user, 'page': "profile"})


@login_required(login_url="login")
def DisplayTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    teamId = user.teamId
    team = get_object_or_404(TeamRegistration, teamId=teamId)
    return render(request, 'accounts/myTeam.html', {'profile_team': team, 'profile_user': user, 'page': "team"})


@login_required(login_url="login")
def leaveTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    user.teamId = None
    user.save()
    return redirect('main:home')


@login_required(login_url="login")
def joinTeam(request):
    user = request.user
    if request.method == 'POST':
        teamId = request.POST.get('teamId')
        if user is not None:
            user = get_object_or_404(UserProfile, user=user)
            if user.teamId is not None:
                message = "You are already in team {}".format(user.teamId)
                message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                return HttpResponse(message, content_type="text/plain")
            team = get_object_or_404(TeamRegistration, teamId=teamId)
            user.teamId = team
            user.save()
            return redirect('accounts:myTeam')
        return reverse('login')
    return render(request, 'accounts/joinTeam.html')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
