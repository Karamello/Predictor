from nfl.models import Team
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('nflteamdata.txt', 'r') as f:
            for t1 in f:

                name, initials, short_name = t1.strip().split(",")
                newteam = Team(name=name, initials=initials, short_name=short_name)
                newteam.save()
