import logging
import math
import time
from datetime import datetime

from constants import RUN_BUCKETS_MAX, TIER_P990, TIER_P999, TIERS
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

        cutoff_by_tier: dict[str, CutoffStats] = {
            tier: RaiderService.get_cutoff_player_count(season, region, tier) for tier in TIERS
        }
        if cap:
            for cutoff_stats in cutoff_by_tier.values():
                cutoff_stats.num_eligible = cap
        for tier, cutoff_stats in cutoff_by_tier.items():
            logger.info(f'Cutoff stats for {tier} retreived: {vars(cutoff_stats)}')

        fetch_cutoff = cutoff_by_tier[TIER_P990]
        characters: list[Character] = self._get_character_data(fetch_cutoff, season, region)

        now = datetime.now()
        date_str = now.strftime('%m-%d-%Y')
        time_str = now.strftime('%H:%M:%S')
        timestamp = now.timestamp()

        for tier in TIERS:
            cutoff_stats = cutoff_by_tier[tier]
            logger.info(f'Building snapshot for {tier}')

            class_data: dict[str, ClassData] = self._get_role_stats(characters, cutoff_stats)
            dungeon_stats: list = self._calculate_dungeon_stats(characters, cutoff_stats, region, season)
            score_list: list[int] = self._get_score_list(characters, cutoff_stats.num_eligible)

            snapshot_doc = MythicPlusSnapshot(
                date_str,
                time_str,
                timestamp,
                region.value,
                season,
                tier,
                cutoff_stats.num_eligible,
                cutoff_stats.cutoff_score,
                cutoff_stats.change,
                cutoff_stats.change_days,
                dungeon_stats,
                class_data,
                score_list
            )

            logger.info(f'Saving {tier} stats snapshot to database')
            self.ss_repo.add_snapshot_document(snapshot_doc)

        logger.info('Snapshot refresh complete')

    def get_latest_snapshot(self, region: str, tier: str = TIER_P999):
        return self.ss_repo.get_latest_snapshot_document(region, tier)

    @staticmethod
    def _get_character_data(cutoff_stats: CutoffStats, season: str, region: Region) -> list[Character]:
        num_chars_to_fetch = cutoff_stats.num_eligible
        page_size: int = None
        total_pages: int = None
        progress_interval: int = 1

        logger.info(
            f'Fetching rankings for {region.value}: '
            f'target {num_chars_to_fetch} characters'
        )

        index: int = 0
        characters: list[Character] = []

        while len(characters) < num_chars_to_fetch:
            rankings_page = RaiderService.get_rankings_page(index, season, region)
            if page_size is None:
                page_size = rankings_page.page_size
                total_pages = math.ceil(num_chars_to_fetch / page_size)
                progress_interval = max(1, total_pages // 10)

            remaining = num_chars_to_fetch - len(characters)
            characters.extend(rankings_page.characters[:remaining])
            index += 1

            if index == 1 or index % progress_interval == 0 or len(characters) >= num_chars_to_fetch:
                logger.info(
                    f'Fetching rankings for {region.value}: '
                    f'{index}/{total_pages} pages ({len(characters)}/{num_chars_to_fetch} characters, '
                    f'page size {page_size})'
                )

            time.sleep(0.05)

        logger.info(
            f'Rankings fetch complete for {region.value}: '
            f'{len(characters)} characters from {index} pages'
        )
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
                dungeon_dict[dungeon.short_name]['runList'].append(
                    SnapshotService._format_run_entry(run['mythicLevel'], run['clearTimeMs'])
                )

                # Use the per-run score provided by Raider (if present) so that
                # each dungeon's averageScore reflects performance specifically in that dungeon.
                run_score = run.get('score')
                if run_score is not None:
                    dungeon_dict[dungeon.short_name]['scoreSum'] += float(run_score)
                    dungeon_dict[dungeon.short_name]['scoreCount'] += 1

        dungeon_stats: list[dict] = []
        for dungeon_entry in dungeon_dict.values():
            score_count = dungeon_entry.get('scoreCount', 0)
            dungeon_entry['averageScore'] = (dungeon_entry['scoreSum'] / score_count) if score_count else 0
            dungeon_entry.pop('scoreSum', None)
            dungeon_entry.pop('scoreCount', None)
            dungeon_entry['runList'], dungeon_entry['runBuckets'] = SnapshotService._bucket_run_list(
                dungeon_entry['runList']
            )
            dungeon_stats.append(dungeon_entry)

        # Highest averageScore first.
        return sorted(dungeon_stats, key=lambda d: d.get('averageScore', 0), reverse=True)

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
    def _get_score_list(characters: list[Character], limit: int = None) -> list[int]:
        score_list = []
        for character in characters[0:limit]:
            score_list.append(round(character.score))
        return score_list

    @staticmethod
    def _format_run_entry(level: int, time_ms: int) -> str:
        time_sec = round(time_ms / 1000)
        return f"{level}-{time_sec}"

    @staticmethod
    def _bucket_run_list(run_list: list[str], max_buckets: int = RUN_BUCKETS_MAX) -> tuple[list[str], int]:
        total = len(run_list)
        if total == 0:
            return [], 0
        if total <= max_buckets:
            return run_list, total

        last_index = total - 1
        bucketed = [
            run_list[round(i * last_index / (max_buckets - 1))]
            for i in range(max_buckets)
        ]
        return bucketed, max_buckets

    @staticmethod
    def _get_empty_dungeon_entry(dungeon):
        return {
            'runs': {},
            'runList': [],
            'runBuckets': 0,
            'scoreSum': 0.0,
            'scoreCount': 0,
            'info': {key.replace('_', ''): value for key, value in dungeon.__dict__.items()}
        }
