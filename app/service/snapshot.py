from service.raider import RaiderService
from repository.firestore import FirestoreRepository
from constants import DF_S3, REGION_US, DF_S3_DUNGEONS, FORT, TYRAN, PAGE_SIZE, AFFIX_MAP
import time
from datetime import datetime
import logging

logger = logging.getLogger('snapshot.service')


class SnapshotService:

    def __init__(self):
        self.ss_repo = FirestoreRepository()

    def generate_new_snapshot(self):
        logger.info('Starting snapshot')
        num_eligible = RaiderService.get_cutoff_player_count(DF_S3, REGION_US)
        logger.info(f'Number of title players retreived: {num_eligible}')

        characters = []
        num_toons = 0
        index = 0
        while num_toons < num_eligible:
            logger.info(f'Getting rankings page {index} for {DF_S3} {REGION_US}')
            character_data = RaiderService.get_rankings_page(index, DF_S3, REGION_US)
            if num_eligible - num_toons > PAGE_SIZE:
                characters = characters + character_data
            else:
                characters = characters + character_data[0: num_eligible - num_toons]
            num_toons += PAGE_SIZE
            index += 1
            time.sleep(0.05)

        modified_characters = []
        logger.info('Trimming down character dataset to remove unused data')
        for character in characters:
            mod_char = {}
            mod_char['character'] = f"{character['name']} - {character['realm']} - {character['region']}"
            mod_char[TYRAN] = {}
            mod_char[FORT] = {}
            for run in character['runs'] + character['alternate_runs']:
                affix = AFFIX_MAP[run['affixes'][0]]
                mod_char[affix][str(run['zoneId'])] = run['mythicLevel']
            modified_characters.append(mod_char)

        scan_doc = {
            'date': datetime.now().strftime('%m-%d-%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().timestamp(),
            'region': REGION_US,
            'season': DF_S3,
            'characters': modified_characters
        }

        logger.info('Saving scan data to database')
        self.ss_repo.add_scan_document(scan_doc)
        logger.info('Calculating stats from dataset')
        snapshot_doc = self._calculate_stats(scan_doc)
        # print(snapshot_doc)
        logger.info('Saving stats snapshot to database')
        self.ss_repo.add_snapshot_document(snapshot_doc)

    def get_latest_snapshot(self):
        return self.ss_repo.get_latest_snapshot_document()

    @staticmethod
    def _calculate_stats(ss_doc):
        logger.info('Getting dungeon info')
        dungeon_map = RaiderService.get_dungeons()
        dungeon_dict = {}
        for character in ss_doc['characters']:
            for affix in FORT, TYRAN:
                for dungeon_id in character[affix].keys():
                    dungeon = dungeon_map[dungeon_id]

                    if dungeon.short_name not in dungeon_dict:
                        dungeon_dict[dungeon.short_name] = SnapshotService._get_empty_dungeon_entry(dungeon)

                    val = str(character[affix][dungeon_id])
                    dungeon_dict[dungeon.short_name][affix][val] = dungeon_dict[dungeon.short_name][affix].get(val, 0) + 1

        return {
            'date': datetime.now().strftime('%m-%d-%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().timestamp(),
            'region': REGION_US,
            'season': DF_S3,
            'dungeons': list(dungeon_dict.values())
        }

    @staticmethod
    def _get_empty_dungeon_entry(dungeon):
        return {
            TYRAN: {},
            FORT: {},
            "info": {key.replace('_', ''): value for key, value in dungeon.__dict__.items()}
        }
