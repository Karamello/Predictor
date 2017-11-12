from django.shortcuts import render
from .models import Team

# Create your views here.

def showteams(request):
    teams = Team.objects.all()
    return render(request, 'nfl/teams.html',{'teams':teams})