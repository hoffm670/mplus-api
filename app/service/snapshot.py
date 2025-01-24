import logging
import time
from datetime import datetime

from constants import PAGE_SIZE
from models.character import Character
from models.cutoff_stats import CutoffStats
from models.dungeon import Dungeon
from models.regions import Region
from models.snapshot import MythicPlusSnapshot
from models.wow_class import ClassData
from repository.firestore import FirestoreRepository
from service.raider import RaiderService

logger = logging.getLogger('snapshot.service')


class SnapshotService:

    def __init__(self):
        self.ss_repo = FirestoreRepository()

    def generate_snapshot_all_regions(self, season: str):
        for region in Region:
            self.generate_new_snapshot(region, season)

    def generate_new_snapshot(self, region: Region, season: str, cap: int = None):
        logger.info(f'Starting snapshot for {season} {region.value}')

        cutoff_stats: CutoffStats = RaiderService.get_cutoff_player_count(season, region)
        if cap:
            # override num_eligible for testing to minimize api calls
            cutoff_stats.num_eligible = cap
        logger.info(f'Cutoff stats title players retreived: {vars(cutoff_stats)}')

        logger.info('Fetching character data')
        characters: list[Character] = self._get_character_data(cutoff_stats, season, region)

        logger.info('Calculating class stats')
        class_data: dict[str, ClassData] = self._get_role_stats(characters, cutoff_stats)

        logger.info('Calculating dungeon stats')
        dungeon_stats: list = self._calculate_dungeon_stats(characters, cutoff_stats, region, season)

        logger.info('Generating score list')
        score_list: list[float] = self._get_score_list(characters)

        snapshot_doc = MythicPlusSnapshot(
            datetime.now().strftime('%m-%d-%Y'),
            datetime.now().strftime('%H:%M:%S'),
            datetime.now().timestamp(),
            region.value,
            season,
            cutoff_stats.num_eligible,
            cutoff_stats.cutoff_score,
            cutoff_stats.change,
            cutoff_stats.change_days,
            dungeon_stats,
            class_data,
            score_list
        )

        logger.info('Saving stats snapshot to database')
        self.ss_repo.add_snapshot_document(snapshot_doc)

        logger.info('Snapshot refresh complete')

    def get_latest_snapshot(self, region: str):
        return self.ss_repo.get_latest_snapshot_document(region)

    @staticmethod
    def _get_character_data(cutoff_stats: CutoffStats, season: str, region: Region) -> list[Character]:
        num_toons: int = 0
        index: int = 0
        characters: list[Character] = []

        num_chars_to_fetch = cutoff_stats.num_eligible * 3
        while num_toons < num_chars_to_fetch:
            logger.info(f'Getting rankings page {index}')
            character_data: list[Character] = RaiderService.get_rankings_page(index, season, region)
            if num_chars_to_fetch - num_toons > PAGE_SIZE:
                characters = characters + character_data
            else:
                characters = characters + character_data[0: num_chars_to_fetch - num_toons]
            num_toons += PAGE_SIZE
            index += 1
            time.sleep(0.05)

        return characters

    @staticmethod
    def _calculate_dungeon_stats(characters: list[Character], cutoff_stats: CutoffStats, region: Region, season: str) -> list:
        dungeon_map: dict[str, Dungeon] = RaiderService.get_dungeons()
        dungeon_dict = {}
        title_characters: list[Character] = characters[0:cutoff_stats.num_eligible]
        for character in title_characters:
            for run in character.runs:
                dungeon_id: str = str(run['zoneId'])
                dungeon: Dungeon = dungeon_map[dungeon_id]

                if dungeon.short_name not in dungeon_dict:
                    dungeon_dict[dungeon.short_name] = SnapshotService._get_empty_dungeon_entry(dungeon)

                key_level = str(run['mythicLevel'])
                dungeon_dict[dungeon.short_name]['runs'][key_level] = dungeon_dict[dungeon.short_name]['runs'].get(key_level, 0) + 1
        return list(dungeon_dict.values())

    @staticmethod
    def _get_role_stats(characters: list[Character], cutoff_stats: CutoffStats) -> dict[str, ClassData]:
        role_dict: dict[str, ClassData] = {}
        for character in characters[0:cutoff_stats.num_eligible]:
            class_key = f"{character.role['name']}-{character.wow_class}"
            if class_key not in role_dict:
                role_dict[class_key] = ClassData(1, character.wow_class, character.role['name'], character.role['role'])
            else:
                role_dict[class_key].count = role_dict[class_key].count + 1
        return role_dict

    @staticmethod
    def _get_score_list(characters: list[Character]) -> list[float]:
        score_list = []
        for character in characters:
            score_list.append(character.score)
        return score_list

    @staticmethod
    def _get_empty_dungeon_entry(dungeon):
        return {
            'runs': {},
            'info': {key.replace('_', ''): value for key, value in dungeon.__dict__.items()}
        }
