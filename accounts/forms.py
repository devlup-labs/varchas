from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import UserProfile
from registration.models import CampusAmbassador


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' ', 'icon': 'a'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    phone = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    college = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'mdb-autocomplete', 'maxlength': '128', 'placeholder': ' '}),
        required=True)
    state = forms.ChoiceField(choices=UserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))

    accommodation_required = forms.ChoiceField(choices=UserProfile.ACCOMMODATION_CHOICES,
                                               widget=forms.Select(attrs={'class': 'mdb-select'}), required=False)
    referred_by = forms.CharField(
        max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder': ' '}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name',
                  'username']

    def clean_first_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['first_name'].capitalize()

    def clean_phone(self):
        _dict = super(RegisterForm, self).clean()
        if not _dict['phone'].isdigit():
            raise forms.ValidationError('Phone number invalid')
        _dict['phone'] = _dict['phone'][-10:]
        return _dict['phone']

    def clean_last_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def clean_referred_by(self):
        _referred_by = "".join(self.data['referred_by'].split()).upper()
        if self.data['referred_by'] == '':
            return None
        elif not CampusAmbassador.objects.filter(referral_code=_referred_by).exists():
            raise forms.ValidationError(
                'This is not a valid referral code, check again or leave blank')
        return CampusAmbassador.objects.get(referral_code=_referred_by)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['username'].widget.attrs['icon_name'] = "fa fa-id-card"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"
        self.fields['referred_by'].widget.attrs['icon_name'] = "fa fa-id-badge"


class PasswordResetCaptchaForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': ' ', 'type': 'email', 'maxlength': '254'}))


class GoogleCreateProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['college', 'referral']

    phone = forms.CharField(min_length=10, max_length=13, widget=forms.TextInput(attrs={'placeholder': ' '}))
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True,
                               widget=forms.Select(attrs={'class': 'mdb-select'}))
    state = forms.ChoiceField(choices=UserProfile.STATE_CHOICES, required=True,
                              widget=forms.Select(attrs={'class': 'mdb-select'}))

    accommodation_required = forms.ChoiceField(choices=UserProfile.ACCOMMODATION_CHOICES,
                                               widget=forms.Select(attrs={'class': 'mdb-select'}), required=False)

    def __init__(self, *args, **kwargs):
        super(GoogleCreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs['icon_name'] = "fa fa-phone"
        self.fields['college'].widget.attrs['icon_name'] = "fa fa-university"
        self.fields['referral'].widget.attrs['icon_name'] = "fa fa-id-badge"
