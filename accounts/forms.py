from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from registration.models import CampusAmbassador


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=False)
    password1 = forms.CharField(min_length=8, label=("Password"), strip=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=("Confirm Password"), strip=False,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['first_name'].capitalize()

    def clean_last_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"


class CreateUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'college', 'state', 'accommodation_required', 'referral']

    def clean_phone(self):
        _dict = super(CreateUserProfileForm, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_referral(self):
        _referral = "".join(self.data['referral'].split()).upper()
        if self.data['referral'] == '':
            return None
        elif not CampusAmbassador.objects.filter(referral_code=_referral).exists():
            raise forms.ValidationError(
                'This is not a valid referral code, check again or leave blank')
        return CampusAmbassador.objects.get(referral_code=_referral)

    def __init__(self, *args, **kwargs):
        super(CreateUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"
        self.fields['referral'].widget.attrs['icon_name'] = "fa fa-id-badge"
