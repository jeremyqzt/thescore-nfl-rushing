from django.core.paginator import Paginator

import uuid
from stats.types import NFLRushingStats

from players.models import Player, Position
from teams.models import Team
from stats.models import StatsEvent, StatsProjection, EventTypes
from stats.types import SortByTypes, SortTypes


sort_type_map = {
    SortTypes.TOTAL_RUSHING_YARDS: "yds",
    SortTypes.LONGEST_RUSH: "lng_eq",
    SortTypes.TOTAL_RUSHING_TOUCHDOWN: "td",
}

sort_by_type_map = {
    SortByTypes.ASC: "",
    SortByTypes.DESC: "-",
}


class UUIDService:
    @staticmethod
    def generate_uuid() -> str:
        return uuid.uuid4()


class StatsEventService:
    @staticmethod
    def createEntry(entry: NFLRushingStats, uuid: str, caller: EventTypes) -> StatsEvent:
        msg_pack = entry.to_json()
        uuid = UUIDService.generate_uuid()
        creation_index = 0

        inst = StatsEvent.objects.create(
            uid=uuid,
            index=creation_index,
            event_type=caller,
            event=msg_pack
        )

        return inst


class ProjectionService:
    @staticmethod
    def projectPlayers(event: NFLRushingStats, uuid: str) -> Player:
        name = event.get("Player")

        try:
            inst = Player.objects.get(full_name=name)
        except Player.DoesNotExist:
            inst = Player.objects.create(uid=uuid, full_name=name)

        return inst

    @staticmethod
    def projectTeams(event: NFLRushingStats, uuid: str) -> Team:
        symbol = event.get("Team")

        try:
            inst = Team.objects.get(team_symbol=symbol)
        except Team.DoesNotExist:
            inst = Team.objects.create(uid=uuid, team_symbol=symbol)

        return inst

    @staticmethod
    def projectPosition(event: NFLRushingStats, uuid: str) -> Position:
        position = event.get("Pos")

        try:
            inst = Position.objects.get(position_symbol=position)
        except Position.DoesNotExist:
            inst = Position.objects.create(uid=uuid, position_symbol=position)

        return inst

    @staticmethod
    def projectStats(
        event: NFLRushingStats,
        uuid: str,
        team: Team,
        player: Player,
        position: Position,
        cur_index: int,
    ) -> StatsProjection:

        stats_projection = {
            "index": cur_index,
            "uid": uuid,
            "team": team,
            "player": player,
            "position": position,

            "att_g": event.get("Att/G"),
            "att": event.get("Att"),
            "yds": event.get("Yds"),

            "avg": event.get("Avg"),
            "yds_g": event.get("Yds/G"),
            "td": event.get("TD"),
            "lng": event.get("Lng"),
            "first_down": event.get("1st"),
            "first_down_pct": event.get("1st%"),
            "yard_20_p": event.get("20+"),
            "yard_40_p": event.get("40+"),
            "fum": event.get("FUM"),
        }

        if cur_index == 0:
            inst = StatsProjection(**stats_projection)
            inst.save()
        else:
            inst = StatsProjection.objects.filter(
                uid=uuid).update(**stats_projection)

        return inst

    @staticmethod
    def getAllStats(sort_on: SortTypes, sort_by: SortByTypes, name_filter: str, page: int, page_size: int):
        all_stat_qs = StatsProjection.objects.all()

        if sort_on is not None and sort_by is not None:
            sort_query = "%s%s" % (
                sort_by_type_map[sort_by], sort_type_map[sort_on])
            all_stat_qs = all_stat_qs.order_by(sort_query)

        if name_filter:
            all_stat_qs = all_stat_qs.filter(
                player__full_name__icontains=name_filter)

        if (page != 0 and page_size != 0):
            return Paginator(all_stat_qs, page_size).page(page).object_list, all_stat_qs.count()

        return all_stat_qs, all_stat_qs.count()
