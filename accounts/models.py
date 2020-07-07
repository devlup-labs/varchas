from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from .utils import unique_ca_referral_code
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


class UserProfile(models.Model):
    ACCOMMODATION_CHOICES = (
        ('N', 'No'),
        ('Y', 'Yes'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )
    DAYS_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
        ('4', 'Four'),
    )
    STATE_CHOICES = (
        ('1', 'Andhra Pradesh'),
        ('2', 'Arunachal Pradesh'),
        ('3', 'Assam'),
        ('4', 'Bihar'),
        ('5', 'Chhattisgarh'),
        ('6', 'Goa'),
        ('7', 'Gujarat'),
        ('8', 'Haryana'),
        ('9', 'Himachal Pradesh'),
        ('10', 'Jammu & Kashmir'),
        ('11', 'Jharkhand'),
        ('12', 'Karnataka'),
        ('13', 'Kerala'),
        ('14', 'Madhya Pradesh'),
        ('15', 'Maharashtra'),
        ('16', 'Manipur'),
        ('17', 'Meghalaya'),
        ('18', 'Mizoram'),
        ('19', 'Nagaland'),
        ('20', 'Odisha'),
        ('21', 'Punjab'),
        ('22', 'Rajasthan'),
        ('23', 'Sikkim'),
        ('24', 'Tamil Nadu'),
        ('25', 'Telangana'),
        ('26', 'Tripura'),
        ('27', 'Uttarakhand'),
        ('28', 'Uttar Pradesh'),
        ('29', 'West Bengal'),
        ('30', 'Andaman & Nicobar Islands'),
        ('31', 'Delhi'),
        ('32', 'Chandigarh'),
        ('33', 'Dadra & Naagar Haveli'),
        ('34', 'Daman & Diu'),
        ('35', 'Lakshadweep'),
        ('36', 'Puducherry'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='M')
    college = models.CharField(max_length=128)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    accommodation_required = models.CharField(max_length=1, choices=ACCOMMODATION_CHOICES, blank=True)
    accomodation_type = models.CharField(max_length=1, default=1)
    amount_required = models.PositiveSmallIntegerField(default=0, blank=True)
    amount_paid = models.PositiveSmallIntegerField(default=0, blank=True)
    no_of_days = models.CharField(max_length=1, choices=DAYS_CHOICES)
    referral = models.CharField(max_length=7, blank=True, null=True)
    id_issued = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_code', blank=True, null=True)
    teamId = models.CharField(max_length=15, default="NULL")

    def __str__(self):
        return self.user.username
