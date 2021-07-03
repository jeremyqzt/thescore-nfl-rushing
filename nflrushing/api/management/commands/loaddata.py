import json
from django.core.management.base import BaseCommand
from stats.types import NFLRushingStats
from stats.cqrs.commands import CreateStatsCmd
from stats.models import EventTypes


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def load_data(self, json):
        for entry in json:
            stats_entry = NFLRushingStats(json=entry)
            CreateStatsCmd().execute(stats_entry, EventTypes.CREATE_SYSTEM)

    def handle(self, *args, **options):
        file = options['file']
        with open(file) as jsonFile:
            jsonObject = json.load(jsonFile)
            jsonFile.close()
        self.load_data(jsonObject)
