from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=30)
    initials = models.CharField(max_length=3)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Season(models.Model):
    year = models.CharField(max_length=4)
    pretty_year = models.CharField(max_length=8)
    def __str__(self):
        return self.year

class Game(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    type = models.CharField(max_length=4)
    week = models.IntegerField()
    ko = models.DateTimeField()
    nfl_id = models.IntegerField(unique=True, db_index=True)
    status = models.CharField(max_length=3)

    def __str__(self):
        return "{} @ {}".format(self.away_team, self.home_team)

    def in_progress(self):
        return self.ko <= timezone.now() and 'F' not in self.status

    def is_complete(self):
        return 'F' in self.status

    def get_game_status_string(self):
        if self.status == '1':
            return "1st Quarter"
        elif self.status == '2':
            return "2nd Quarter"
        elif self.status == '3':
            return "3rd Quarter"
        else:
            return "4th Quarter"

    def determine_leader(self):
        if self.home_score > self.away_score:
            return 2
        elif self.away_score > self.home_score:
            return 1
        else:
            return 0

class Pick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    choice = models.IntegerField(default=3)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

class Scores(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()