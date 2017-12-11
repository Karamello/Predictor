from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Team, Game, Season, Pick
import xml.etree.ElementTree as et
from urllib import request as urlre
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json



# Create your views here.

def showteams(request):
    teams = Team.objects.all()
    return render(request, 'nfl/teams.html',{'title':'Teams','teams':teams})

def showgames(request, season, week):
    seao = get_object_or_404(Season, year=season)
    games = Game.objects.filter(season=seao,week=week)
    get_list_or_404(games)
    return render(request, 'nfl/games.html', {'title':'Week {} games'.format(week),'games':games, 'season':seao, 'week':week})

@login_required(login_url='/user/login/')
def makepicks(request):
    settings = {}

    with open("static/nfl/config/config.json", "r") as config:
        settings = json.load(config)

    seao = get_object_or_404(Season, year=settings['season'])
    games_list = Game.objects.filter(season=seao, week=settings['week'])
    get_list_or_404(games_list)
    games = []
    for game in games_list:
        pick = Pick.objects.get_or_create(user=request.user, game=game)[0]
        games.append((game, pick))
    return render(request, 'nfl/picks.html', {'title': 'Make your picks', 'season': seao, 'games':games, 'week': settings['week']})

def updategames(request, season, week):
    pot_games = Game.objects.filter(season=Season.objects.get(year=season), week=week).exclude(status__contains='F')
    updates = {}
    for game in pot_games:
        print("DEBUG: {}".format(game))
        if game.in_progress():
            data = urlre.urlopen("http://www.nfl.com/ajax/scorestrip?season={}&seasonType=REG&week={}".format(season, week)).read().decode()

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
                temp['q'] = get_game_status_string(game.status)
                was_modified = True
            if was_modified:
                game.save()
                updates[game.nfl_id] = temp

    return JsonResponse(updates)

def get_game_status_string(status):
    if 'F' in status:
        return "Final"
    elif status == '1':
        return "<b>LIVE - 1st Quarter</b>"
    elif status == '2':
        return "<b>LIVE - 2nd Quarter</b>"
    elif status == '3':
        return "<b>LIVE - 3rd Quarter</b>"
    else:
        return "<b>LIVE - 4th Quarter</b>"

