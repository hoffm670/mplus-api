from service.raider import RaiderService
from repository.firestore import FirestoreRepository
from repository.raider_scraper import RaiderScraper
from constants import DF_S3, REGION_US, DF_S3_DUNGEONS, FORT, TYRAN
import time
from datetime import datetime
import logging

logger = logging.getLogger('snapshot.service')

class SnapshotService:

    def __init__(self):
        self.ss_repo = FirestoreRepository()
        self.scraper = RaiderScraper()

    def generate_new_snapshot(self):
        logger.info('Starting snapshot')
        num_eligible = RaiderService.get_cutoff_player_count(DF_S3, REGION_US)
        # num_eligible = 45
        logger.info(f'Number of title players retreived: {num_eligible}')

        # Run scraper to get list of players
        logger.info(f'Starting to scrape raider.io leaderboard')
        players = self.scraper.get_title_players(
            num_eligible, DF_S3, REGION_US)

        scan_doc = {
            'date': datetime.now().strftime('%m-%d-%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'region': REGION_US,
            'season': DF_S3,
            'characters': []
        }

        # Make calls for each player
        for player in players:
            try:
                res = RaiderService.get_player_highest_keys(
                    player['name'], player['server'], player['region'])
                scan_doc['characters'].append(res)
                time.sleep(0.05)
            except Exception as error:
                logger.error(f'Error {error}')
                logger.error(player)
                logging.info('Sleeping 5 seconds after failed API call...')
                time.sleep(5)



        self.ss_repo.add_scan_document(scan_doc)
        snapshot_doc = self._calculate_stats(scan_doc)
        self.ss_repo.add_snapshot_document(snapshot_doc)

    @staticmethod
    def _calculate_stats(ss_doc):

        dungeon_dict = {}
        for dungeon in DF_S3_DUNGEONS:
            dungeon_dict[dungeon] = {}
            dungeon_dict[dungeon][FORT] = {}
            dungeon_dict[dungeon][TYRAN] = {}

        for character in ss_doc['characters']:
            for affix in FORT, TYRAN:
                for key in character[affix].keys():
                    val = str(character[affix][key])
                    dungeon_dict[key][affix][val] = dungeon_dict[key][affix].get(val, 0) + 1
        
        
        return {
            'date': datetime.now().strftime('%m-%d-%Y'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'region': REGION_US,
            'season': DF_S3,
            'dungeons': dungeon_dict
        }
