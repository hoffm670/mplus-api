import logging
import time
from datetime import datetime

from models.character import Character
from models.dungeon import Dungeon
from constants import PAGE_SIZE
from models.cutoff_stats import CutoffStats
from models.regions import Region
from repository.firestore import FirestoreRepository
from service.raider import RaiderService

logger = logging.getLogger('snapshot.service')


class SnapshotService:

    def __init__(self):
        self.ss_repo = FirestoreRepository()

    def generate_snapshot_all_regions(self, season: str):
        for region in Region:
            self.generate_new_snapshot(region, season)

    def generate_new_snapshot(self, region: Region, season: str):
        logger.info(f'Starting snapshot for {season} {region.value}')
        cutoff_stats: CutoffStats = RaiderService.get_cutoff_player_count(season, region)
        logger.info(f'Cutoff stats title players retreived: {vars(cutoff_stats)}')

        characters: list[Character] = []
        num_toons: int = 0
        index: int = 0
        while num_toons < cutoff_stats.num_eligible:
            logger.info(f'Getting rankings page {index}')
            character_data: list[Character] = RaiderService.get_rankings_page(index, season, region)
            if cutoff_stats.num_eligible - num_toons > PAGE_SIZE:
                characters = characters + character_data
            else:
                characters = characters + character_data[0: cutoff_stats.num_eligible - num_toons]
            num_toons += PAGE_SIZE
            index += 1
            time.sleep(0.05)

        logger.info('Calculating stats from dataset')
        snapshot_doc = self._calculate_stats(characters, cutoff_stats, region, season)

        logger.info('Saving stats snapshot to database')
        self.ss_repo.add_snapshot_document(snapshot_doc)

        logger.info('Snapshot refresh complete')

    def get_latest_snapshot(self, region: str):
        return self.ss_repo.get_latest_snapshot_document(region)

    @staticmethod
    def _calculate_stats(characters: list[Character], cutoff_stats: CutoffStats, region: Region, season: str):
        logger.info('Getting dungeon info')
        dungeon_map: dict[str, Dungeon] = RaiderService.get_dungeons()
        dungeon_dict = {}
        for character in characters:
            for run in character.runs:
                dungeon_id: str = str(run['zoneId'])
                dungeon: Dungeon = dungeon_map[dungeon_id]

                if dungeon.short_name not in dungeon_dict:
                    dungeon_dict[dungeon.short_name] = SnapshotService._get_empty_dungeon_entry(dungeon)

                key_level = str(run['mythicLevel'])
                dungeon_dict[dungeon.short_name]['runs'][key_level] = dungeon_dict[dungeon.short_name]['runs'].get(key_level, 0) + 1

        return {
            'date': datetime.now().strftime('%m-%d-%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().timestamp(),
            'region': region.value,
            'season': season,
            'character_count': cutoff_stats.num_eligible,
            'rating_cutoff': cutoff_stats.cutoff_score,
            'change': cutoff_stats.change,
            'change_days': cutoff_stats.change_days,
            'dungeons': list(dungeon_dict.values()),
        }

    @staticmethod
    def _get_empty_dungeon_entry(dungeon):
        return {
            'runs': {},
            "info": {key.replace('_', ''): value for key, value in dungeon.__dict__.items()}
        }
