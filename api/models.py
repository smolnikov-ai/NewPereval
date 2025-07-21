from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.resources import (CHOICES_LEVEL_DIFFICULTY_PEREVAL,
                           CHOICES_STATUS_MODERATION_PEREVAL)


class User(models.Model):
    email = models.EmailField()
    fam = models.CharField()
    name = models.CharField()
    otc = models.CharField(blank=True, null=True)
    phone = models.CharField(max_length=12)


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, blank=True, null=True)
    summer = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, blank=True, null=True)
    autumn = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, blank=True, null=True)
    spring = models.CharField(choices=CHOICES_LEVEL_DIFFICULTY_PEREVAL, blank=True, null=True)


class Pereval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    beauty_title = models.CharField(blank=True, null=True)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(blank=True, null=True)
    connect = models.CharField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=CHOICES_STATUS_MODERATION_PEREVAL, default='new')


class Images(models.Model):
    data = models.URLField()
    title = models.CharField()
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
