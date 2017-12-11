from nfl.models import Team, Game, Season
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as et
from urllib import request
import datetime
import json

class Command(BaseCommand):
    def parsetime(self, date, time):
        return "{}-{}-{} {}PM -0500".format(date[:4],date[4:6],date[6:8],time)

    def handle(self, *args, **options):
        with open("static/nfl/config/config.json", 'r') as config:
            settings = json.load(config)

        if settings:
            data = request.urlopen("http://www.nfl.com/ajax/scorestrip?season={}&seasonType={}&week={}".format(settings['season'], settings['type'], settings['week'])).read().decode()
            tree = et.ElementTree(et.fromstring(data))
            gms = tree.find('gms')
            week = gms.attrib['w']
            sea = Season.objects.get(year=gms.attrib['y'])
            game_type = 'REG' if gms.attrib['t'] == 'R' else 'POST'
            for gameelement in gms:
                game = gameelement.attrib
                team1 = Team.objects.get(initials=game['v'])
                team2 = Team.objects.get(initials=game['h'])
                timeuk = datetime.datetime.strptime(self.parsetime(game['eid'], game['t']), "%Y-%m-%d %I:%M%p %z")
                home_score = game['hs'] if game['hs'] else 0
                away_score = game['vs'] if game['vs'] else 0
                newgame = Game(home_team=team2, away_team=team1, ko=timeuk, week=week, season=sea, home_score=home_score, away_score=away_score, nfl_id=game['gsis'], status=game['q'], type=game_type)
                print(newgame, team1, team2, timeuk, game['hs'], game['vs'], game['gsis'], game['q'], game_type)
                newgame.save()