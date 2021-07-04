import json
import os
from django.core.management.base import BaseCommand
from stats.types import NFLRushingStats
from stats.cqrs.commands import CreateStatsCmd
from stats.models import EventTypes, StatsEvent


class Command(BaseCommand):
    help = 'Loads json files as seed for the stats DB.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def load_data(self, json, fname):
        for entry in json:
            stats_entry = NFLRushingStats(json=entry)
            CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM, fname)

    def handle(self, *args, **options):
        file = options['file']
        fname = os.path.basename(file)
        # Already Loaded
        count = StatsEvent.objects.filter(fname=fname).count()

        if count > 0:
            print("Already Loaded File")
            return

        with open(file) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        self.load_data(jsonObject, fname)
        print("All data loaded from " + fname)
