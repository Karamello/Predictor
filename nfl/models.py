from django.db import models
from django.conf import settings

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=3)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Season(models.Model):
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.year

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    stadium = models.CharField(max_length=50)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    type = models.CharField(max_length=3)
    week = models.IntegerField()
    ko = models.DateTimeField()

    def __str__(self):
        return "{} @ {}".format(self.away_team, self.home_team)

class Pick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    choice = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

class Scores(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()