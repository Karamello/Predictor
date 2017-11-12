from django.shortcuts import render
from .models import Team, Game

# Create your views here.

def showteams(request):
    teams = Team.objects.all()
    return render(request, 'nfl/teams.html',{'teams':teams})

def showgames(request):
    games = Game.objects.filter(week=10)
    return render(request, 'nfl/games.html', {'games':games})