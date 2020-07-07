from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_save
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

class HomeImageCarousel(models.Model):
    ordering = models.PositiveIntegerField(default=64)
    title = models.CharField(max_length=64)
    image = models.ImageField(
        upload_to='homepage-carousel', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class HomeEventCard(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(
        upload_to='homepage-events', blank=True, null=True)
    link = models.URLField()

    def __str__(self):
        return self.name


class HomeBriefCard(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class NavBarSubOptions(models.Model):
    title = models.CharField(max_length=64)
    description = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    use_custom_html = models.BooleanField(default=False)
    custom_html = models.CharField(max_length=64, blank=True, null=True)

    def clean(self):
        if self.use_custom_html and not self.custom_html:
            raise ValidationError(
                'Custom HTML should be present with Use custom html option')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:navbarsuboptionpage', kwargs={'slug': self.slug})


class NavBarOptions(models.Model):
    title = models.CharField(max_length=64)
    sub_options = models.ManyToManyField(NavBarSubOptions)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(event_pre_save_receiver, sender=NavBarSubOptions)
