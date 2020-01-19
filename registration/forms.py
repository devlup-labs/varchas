from django import forms
from .models import CampusAmbassador, TeamRegistration


class CampusAmbassadorForm(forms.ModelForm):

    class Meta:
        model = CampusAmbassador
        exclude = ['referral_code']

    def clean_name(self):
        return self.data['name'].strip().title()

    def clean_email(self):
        if CampusAmbassador.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']


class TeamRegistrationForm(forms.ModelForm):

    class Meta:
        model = TeamRegistration
        fields = ['sport', 'college']


class TeamRegistrationForm1(forms.ModelForm):

    class Meta:
        model = TeamRegistration
        fields = ['sport', 'teamId', 'college']
