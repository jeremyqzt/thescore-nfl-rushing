from stats.types import NFLRushingStats
from stats.cqrs.services import StatsEventService, ProjectionService, UUIDService
from stats.models import EventTypes


class CreateStatsCmd():
    def execute(self, stats: NFLRushingStats, event_type: EventTypes):
        stats_uuid = UUIDService.generate_uuid()
        new_event = StatsEventService.createEntry(
            stats, stats_uuid, event_type)

        created_event = NFLRushingStats(json=new_event.event, )

        player_uuid = UUIDService.generate_uuid()
        new_player = ProjectionService.projectPlayers(
            created_event, player_uuid)

        team_uuid = UUIDService.generate_uuid()
        new_team = ProjectionService.projectTeams(
            created_event, team_uuid)

        position_uuid = UUIDService.generate_uuid()
        new_position = ProjectionService.projectPosition(
            created_event, position_uuid)

        new_stats = ProjectionService.projectStats(
            created_event, stats_uuid, new_team, new_player, new_position, new_event.index)

        return new_stats
