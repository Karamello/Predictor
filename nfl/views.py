from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Team, Game, Season
import xml.etree.ElementTree as et
from urllib import request as urlre
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

def showteams(request):
    teams = Team.objects.all()
    return render(request, 'nfl/teams.html',{'title':'Teams','teams':teams})

def showgames(request, season, week):
    seao = get_object_or_404(Season, year=season)
    games = Game.objects.filter(season=seao,week=week)
    get_list_or_404(games)
    return render(request, 'nfl/games.html', {'title':'Games','games':games, 'season':seao, 'week':week})

def makepicks(request):
    seao = get_object_or_404(Season, year=2017)
    games = Game.objects.filter(season=seao, week=10)
    get_list_or_404(games)
    return render(request, 'nfl/picks.html', {'title': 'Make your picks', 'games':games, 'week': 10})

def updategames(request):
    pot_games = Game.objects.filter(week=10).exclude(status__contains='F')
    updates = {}
    for game in pot_games:
        if game:
            if 'P' == game.status and timezone.now() <= game.ko:
                continue
            else:
                data = urlre.urlopen("http://www.nfl.com/liveupdate/scorestrip/ss.xml").read().decode()
                tree = et.ElementTree(et.fromstring(data))
                gm = tree.find(".//*[@gsis='{}']".format(game.nfl_id))
                temp = {}
                was_modified = False
                if game.home_score != int(gm.attrib['hs']):
                    game.home_score = gm.attrib['hs']
                    temp['hs'] = game.home_score
                    was_modified = True
                if game.away_score != int(gm.attrib['vs']):
                    game.away_score = gm.attrib['vs']
                    temp['vs'] = game.away_score
                    was_modified = True
                if game.status != gm.attrib['q']:
                    game.status = gm.attrib['q']
                    temp['q'] = game.status
                    was_modified = True
                if was_modified:
                    game.save()
                    updates[game.nfl_id] = temp

    return JsonResponse(updates)