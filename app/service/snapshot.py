import logging
import time
from datetime import datetime

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
        cutoff_stats = RaiderService.get_cutoff_player_count(season, region)
        logger.info(f'Cutoff stats title players retreived: {vars(cutoff_stats)}')

        characters = []
        num_toons = 0
        index = 0
        while num_toons < cutoff_stats.num_eligible:
            logger.info(f'Getting rankings page {index}')
            character_data = RaiderService.get_rankings_page(index, season, region)
            if cutoff_stats.num_eligible - num_toons > PAGE_SIZE:
                characters = characters + character_data
            else:
                characters = characters + character_data[0: cutoff_stats.num_eligible - num_toons]
            num_toons += PAGE_SIZE
            index += 1
            time.sleep(0.05)

        modified_characters = []
        logger.info('Trimming down character dataset to remove unused data')
        for character in characters:
            mod_char = {}
            mod_char['character'] = f"{character['name']} - {character['realm']} - {character['region']}"
            mod_char['runs'] = {}
            for run in character['runs']:
                mod_char['runs'][str(run['zoneId'])] = run['mythicLevel']
            modified_characters.append(mod_char)

        logger.info('Calculating stats from dataset')
        snapshot_doc = self._calculate_stats(modified_characters, cutoff_stats, region, season)

        logger.info('Saving stats snapshot to database')
        self.ss_repo.add_snapshot_document(snapshot_doc)

        logger.info('Snapshot refresh complete')

    def get_latest_snapshot(self, region: str):
        return self.ss_repo.get_latest_snapshot_document(region)

    @staticmethod
    def _calculate_stats(characters, cutoff_stats: CutoffStats, region: Region, season: str):
        logger.info('Getting dungeon info')
        dungeon_map = RaiderService.get_dungeons()
        dungeon_dict = {}
        for character in characters:
            for dungeon_id in character['runs'].keys():
                dungeon = dungeon_map[dungeon_id]

                if dungeon.short_name not in dungeon_dict:
                    dungeon_dict[dungeon.short_name] = SnapshotService._get_empty_dungeon_entry(dungeon)

                val = str(character['runs'][dungeon_id])
                dungeon_dict[dungeon.short_name]['runs'][val] = dungeon_dict[dungeon.short_name]['runs'].get(val, 0) + 1

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
