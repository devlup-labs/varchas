from django.db.models.signals import pre_save
from django.db import models
from .utils import unique_ca_referral_code
from accounts.models import UserProfile
from django.core.mail import send_mail


class CampusAmbassador(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    college = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=13)
    fb_link = models.CharField(max_length=80, default='facebook.com')
    publicize_varchas = models.CharField(max_length=512, blank=True)
    past_experience = models.TextField(max_length=512)
    referral_code = models.CharField(max_length=7, editable=False)

    def __str__(self):
        return self.name


def pre_save_campus_ambassador(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.referral_code = unique_ca_referral_code(instance)

        message = '''<!DOCTYPE html> <html><body>Hey {}!<br>You are now team Varchas.<br>Your referral code is: <b>{}</b><br>
                     Spread the referral code, get more registrations from your code to win exciting prizes<p>Get Your Game
                      On.</p></body></html>'''.format(instance.name, instance.referral_code)
        send_mail('Varchas CA Referral Code', message, 'noreply@varchas2020.org', [instance.email],
                  fail_silently=False, html_message=message)


pre_save.connect(pre_save_campus_ambassador, sender=CampusAmbassador)


class TeamRegistration(models.Model):
    SPORT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Chess'),
        ('5', 'Cricket'),
        ('6', 'Football'),
        ('7', 'Table Tenis'),
        ('8', 'Tenis'),
        ('9', 'Volleyball'),
    )
    teamId = models.CharField(max_length=15, unique=True, blank=True)
    sport = models.CharField(max_length=2, choices=SPORT_CHOICES)
    college = models.CharField(max_length=128)
    captian = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.teamId
