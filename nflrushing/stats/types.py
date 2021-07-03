from enum import Enum

from stats.exceptions import InvalidStatsObject


class SortTypes(Enum):
    TOTAL_RUSHING_YARDS = 1
    LONGEST_RUSH = 2
    TOTAL_RUSHING_TOUCHDOWN = 3


class SortByTypes(Enum):
    ASC = 1
    DESC = 2


class NFLRushingStats(object):
    def __init__(self, json=None, statsProjection=None):
        if ((json == None) == (statsProjection == None)):
            raise InvalidStatsObject

        if (json is not None):
            self.json = self._clean_json(json)

        if (statsProjection is not None):
            self._from_model(statsProjection)

    def _clean_json(self, json):
        int_fields = ["Att", "Yds", "TD", "20+", "40+", "FUM", "1st"]
        for key in json:
            if key in int_fields and not isinstance(json[key], int):
                json[key] = int(json[key].replace(',', ''))

        return json

    def _from_model(self, inst):
        self.json = {
            "Player": inst.player.full_name,
            "Team": inst.team.team_symbol,
            "Pos": inst.position.position_symbol,

            "Att": inst.att,
            "Att/G": inst.att_g,
            "Yds": inst.yds,
            "Avg": inst.avg,
            "Yds/G": inst.yds_g,
            "TD": inst.td,
            "Lng": inst.lng,
            "1st": inst.first_down,
            "1st%": inst.first_down_pct,
            "20+": inst.yard_20_p,
            "40+": inst.yard_40_p,
            "FUM": inst.fum,
        },

    def to_json(self):
        return self.json

    def __get__(self, key):
        return self.get(key)

    def get(self, key):
        return self.json.get(key, None)
