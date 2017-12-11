from django.core.management.base import BaseCommand
import xml.etree.ElementTree as et
from urllib import request as url
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        data = url.urlopen("http://www.nfl.com/liveupdate/scorestrip/ss.xml").read().decode()
        tree = et.ElementTree(et.fromstring(data))
        gms = tree.find('gms')
        week = gms.attrib['w']
        sea = gms.attrib['y']
        game_type = 'REG' if gms.attrib['t'] == 'R' else 'POST'

        with open("static/nfl/config/config.json", 'w') as config:
            output = {'season': sea, 'week': week, 'type': game_type}
            json.dump(output, config, indent=4)

