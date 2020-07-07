from django import forms
from .models import Team
from accounts.models import CampusAmbassador


class CampusAmbassadorForm(forms.ModelForm):
    class Meta:
        model = CampusAmbassador
        exclude = ['referral_code']

    def clean_name(self):
        return self.data['name']

    def clean_email(self):
        if CampusAmbassador.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def clean_phone(self):
        _dict = super(CampusAmbassadorForm, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def __init__(self, *args, **kwargs):
        super(CampusAmbassadorForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['fb_link'].widget.attrs['icon_name'] = "fa fa-facebook"
        self.fields['address'].widget.attrs['icon_name'] = "fa fa-address-card"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"
        self.fields['past_experience'].widget.attrs['icon_name'] = "fa fa-file-text"
        self.fields['publicize_varchas'].widget.attrs['icon_name'] = " fa fa-globe"


class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['sport', 'college']


class TeamRegistrationForm1(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['sport', 'teamId', 'college']

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm1, self).__init__(*args, **kwargs)
        self.fields['teamId'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"


class RemovePlayerForm(forms.Form):
    player = forms.EmailField()
