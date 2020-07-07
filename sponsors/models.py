from django.db import models


class SponsorType(models.Model):
    name = models.CharField(max_length=128)
    order = models.PositiveIntegerField(default=64)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='sponsor')
    sponsor_type = models.ForeignKey(SponsorType, on_delete=models.CASCADE)
    link = models.URLField(help_text="Sponsor's website url", null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sponsor_type__order', 'name']
