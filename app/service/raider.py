from datetime import datetime, time

from models.character import Character
from models.cutoff_stats import CutoffStats
from models.dungeon import Dungeon
from models.regions import Region
from repository.raider_api import RaiderApi


class RaiderService:

    @staticmethod
    def get_cutoff_player_count(season, region: Region) -> CutoffStats:
        api_response = RaiderApi.get_season_cutoff(season, region.value)
        player_count = api_response["cutoffs"]["p999"]["all"]["quantilePopulationCount"]
        cutoff_rating = api_response["cutoffs"]["p999"]["all"]["quantileMinValue"]
        graphData = api_response["cutoffs"]["graphData"]["p999"]["data"]
        if graphData:
            latest_ts = datetime.combine(datetime.fromtimestamp(graphData[0]['x'] / 1000), time.min)
            change = change_days = 0
            for entry in graphData:
                ts = datetime.combine(datetime.fromtimestamp(entry['x'] / 1000), time.min)

                days_diff = abs(latest_ts - ts).days
                if days_diff >= 7:
                    change = round(cutoff_rating - entry['y'], 1)
                    change_days = days_diff
                    break
        else:
            change = 0
            change_days = 7

        return CutoffStats(cutoff_rating, player_count, change, change_days)

    @staticmethod
    def get_player_highest_keys(name, realm, region):
        api_response = RaiderApi.get_character_profile(name, realm, region)
        best_keys = {}
        best_keys['character'] = f'{name} - {realm} - {region}'
        best_keys['runs'] = {}
        for run in api_response['mythic_plus_best_runs']:
            short_name = run['short_name']
            best_keys['runs'][short_name] = run['mythic_level']
        return (best_keys)

    @staticmethod
    def get_rankings_page(page, season, region: Region) -> list[Character]:
        api_response = RaiderApi.get_rankings_page(page, season, region.value)
        characters = api_response['rankings']['rankedCharacters']
        trimmed_data: list[Character] = []
        for character in characters:
            trimmed_data.append(Character(
                character['character']['name'],
                character['character']['realm']['name'],
                character['character']['region']['slug'],
                character['character']['class']['name'],
                character['character']['spec'],
                character['runs'],
                character['score']
            ))
        return trimmed_data

    @staticmethod
    def get_dungeons() -> dict[str, Dungeon]:
        api_response = RaiderApi.get_expansion_dungeon_data()
        seasons: dict = api_response['seasons']
        dungeons_list = []
        for season in seasons:
            if season['dungeons']:
                dungeons_list = dungeons_list + season['dungeons']
        dungeon_map = RaiderService._create_dungeon_map(dungeons_list)
        return dungeon_map

    @staticmethod
    def _create_dungeon_map(dungeons_json) -> dict[str, Dungeon]:
        dungeon_map = {}
        for entry in dungeons_json:
            dungeon = Dungeon(entry['id'], entry['slug'], entry['name'], entry['short_name'])
            dungeon_map[str(dungeon.id)] = dungeon
        return dungeon_map
