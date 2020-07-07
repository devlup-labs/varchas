from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class OurTeam(models.Model):
    POSITION_CHOICES = (
        (1, 'Festival Chief'),
        (2, 'Finance Head'),
        (3, 'Creativity'),
        (4, 'Informals'),
        (5, 'Marathon'),
        (6, 'Marketing'),
        (7, 'Public Relations and Hospitality'),
        (8, 'Publicity and Media'),
        (9, 'Pronite'),
        (10, 'Resources'),
        (11, 'Security'),
        (12, 'SOCH'),
        (13, 'Sport Coordinator'),
        (14, 'Transport'),
        (15, 'Web and APP'),
    )
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10, validators=[contact])
    position = models.IntegerField(choices=POSITION_CHOICES)
    picture = models.ImageField(
        upload_to='teamPics/', blank=True, null=True, default="teamPics/default.jpg")
    insta = models.URLField(max_length=100, null=True, blank=True)
    fp = models.URLField(max_length=100, null=True, blank=True)
    linkedIn = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']


class AdminProfile(models.Model):
    DEPARTMENT_CHOICES = (
        ('NONE', 'None'),
        ('FLAG', 'Flagship'),
        ('ONL9', 'Online'),
        ('PUBR', 'Public Relations'),
        ('MAR', 'Marketing'),
        ('EVNT', 'Sports Events'),
    )

    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                verbose_name='username')
    phone = models.CharField(max_length=10, validators=[contact])
    department = models.CharField(choices=DEPARTMENT_CHOICES, default='NONE', max_length=8)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.get_full_name()


class DepartmentTeam(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(AdminProfile, through='DepartmentTeamMembership',
                                     through_fields=('department_team', 'profile'))
    hierarchy = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['hierarchy']

    def __str__(self):
        return self.name


class DepartmentTeamMembership(models.Model):
    department_team = models.ForeignKey(DepartmentTeam, on_delete=models.CASCADE)
    profile = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    hierarchy = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['hierarchy']

    def __str__(self):
        return self.profile.name


class email(models.Model):
    RECIPIENT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Chess'),
        ('5', 'Cricket'),
        ('6', 'Football'),
        ('7', 'Table Tenis'),
        ('8', 'Tenis'),
        ('9', 'Volleyball'),
        ('10', 'CA'),
        ('11', 'All Teams'),
        ('12', 'All Users'),
    )
    recipient = models.CharField(max_length=3, choices=RECIPIENT_CHOICES)
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=180)
