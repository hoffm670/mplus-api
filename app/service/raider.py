from repository.raider_api import RaiderApi
from models.dungeon import Dungeon
from models.cutoff_stats import CutoffStats
from models.regions import Region
from constants import FORT, TYRAN
from datetime import datetime, time


class RaiderService:

    @staticmethod
    def get_cutoff_player_count(season, region: Region) -> CutoffStats:
        api_response = RaiderApi.get_season_cutoff(season, region.value)
        player_count = api_response["cutoffs"]["p999"]["all"]["quantilePopulationCount"]
        cutoff_rating = api_response["cutoffs"]["p999"]["all"]["quantileMinValue"]
        graphData = api_response["cutoffs"]["graphData"]["p999"]["data"]
        latest_ts = datetime.combine(datetime.fromtimestamp(graphData[0]['x'] / 1000), time.min)
        change = change_days = 0
        for entry in graphData:
            ts = datetime.combine(datetime.fromtimestamp(entry['x'] / 1000), time.min)

            days_diff = abs(latest_ts - ts).days
            if days_diff >= 7:
                change = round(cutoff_rating - entry['y'], 1)
                change_days = days_diff
                break

        return CutoffStats(cutoff_rating, player_count, change, change_days)

    @staticmethod
    def get_player_highest_keys(name, realm, region):
        api_response = RaiderApi.get_character_profile(name, realm, region)
        best_keys = {}
        best_keys['character'] = f'{name} - {realm} - {region}'
        best_keys[TYRAN] = {}
        best_keys[FORT] = {}
        for run in api_response['mythic_plus_best_runs'] + api_response['mythic_plus_alternate_runs']:
            affix = run['affixes'][0]['name']
            short_name = run['short_name']
            best_keys[affix][short_name] = run['mythic_level']
        return (best_keys)

    @staticmethod
    def get_rankings_page(page, season, region: Region):
        api_response = RaiderApi.get_rankings_page(page, season, region.value)
        characters = api_response['rankings']['rankedCharacters']
        trimmed_data = []
        for character in characters:
            trimmed_data.append({
                "name": character['character']['name'],
                "realm": character['character']['realm']['name'],
                "region": character['character']['region']['slug'],
                "runs": character['runs'],
                "alternate_runs": character['alternateRuns']
            })
        return trimmed_data

    @staticmethod
    def get_dungeons() -> dict[str, Dungeon]:
        api_response = RaiderApi.get_expansion_dungeon_data()
        seasons = api_response['seasons']
        dungeons_json = next(season for season in seasons if season['slug'])['dungeons']
        dungeon_map = RaiderService._create_dungeon_map(dungeons_json)
        return dungeon_map

    @staticmethod
    def _create_dungeon_map(dungeons_json) -> dict[str, Dungeon]:
        dungeon_map = {}
        for entry in dungeons_json:
            dungeon = Dungeon(entry['id'], entry['slug'], entry['name'], entry['short_name'])
            dungeon_map[str(dungeon.id)] = dungeon
        return dungeon_map
