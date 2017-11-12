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
        root = tree.getroot()
        for child in root:
            week = child.attrib['w']
            sea = Season.objects.get(year="2017")
            for gameelement in child:
                game = gameelement.attrib
                team1 = Team.objects.get(initials=game['v'])
                team2 = Team.objects.get(initials=game['h'])
                timeuk = datetime.datetime.strptime(self.parsetime(game['eid'], game['t']), "%Y-%m-%d %I:%M%p %z")
                newgame = Game(home_team=team2, away_team=team1, ko=timeuk, week=week, season=sea, home_score=game['hs'], away_score=game['vs'])
                newgame.save()