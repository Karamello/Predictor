from nfl.models import Team, Game, Season
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as et
from urllib import request
import datetime

class Command(BaseCommand):
    def parsetime(self, date, time):
        return "{}-{}-{} {}PM -0500".format(date[:4],date[4:6],date[6:8],time)

    def handle(self, *args, **options):
        data = request.urlopen("http://www.nfl.com/liveupdate/scorestrip/ss.xml").read().decode()
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
            newgame = Game(home_team=team2, away_team=team1, ko=timeuk, week=week, season=sea, home_score=game['hs'], away_score=game['vs'], nfl_id=game['gsis'], status=game['q'], type=game_type)
            newgame.save()