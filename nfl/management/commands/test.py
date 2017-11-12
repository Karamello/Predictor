from nfl.models import Game
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as et
from urllib import request


class Command(BaseCommand):
    def parsetime(self, date, time):
        return "{}-{}-{} {}PM -0500".format(date[:4],date[4:6],date[6:8],time)

    def handle(self, *args, **options):
        data = request.urlopen("http://www.nfl.com/liveupdate/scorestrip/ss.xml").read().decode()
        tree = et.ElementTree(et.fromstring(data))
        gms = tree.find('gms')
        for element in gms:
            game = Game.objects.get(nfl_id=element.attrib['gsis'])
            if game and 'F' not in game.status:
                if game.home_score != element.attrib['hs']:
                    game.home_score = element.attrib['hs']
                if game.away_score != element.attrib['vs']:
                    game.away_score = element.attrib['vs']
                if game.status != element.attrib['q']:
                    game.status = element.attrib['q']
                game.save()