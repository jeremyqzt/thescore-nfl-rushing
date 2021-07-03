from stats.types import SortByTypes, SortTypes
from stats.cqrs.services import ProjectionService
from stats.types import NFLRushingStats


class GetAllStatsQuery():
    def execute(self, sort_on: SortTypes, sort_by: SortByTypes, name_filter: str, page: int, page_size: int):

        all_stats, total = ProjectionService.getAllStats(
            sort_on, sort_by, name_filter, page, page_size)

        ret_paged_stats = [NFLRushingStats(
            statsProjection=obj).to_json() for obj in all_stats]
        return ret_paged_stats, total
