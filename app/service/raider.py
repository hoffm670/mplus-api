from repository.raider_api import RaiderApi
from models.dungeon import Dungeon
from constants import FORT, TYRAN, CURRENT_SEASON


class RaiderService:
    
    @staticmethod
    def get_cutoff_player_count(season, region):
        api_response = RaiderApi.get_season_cutoff(season, region)
        player_count = api_response["cutoffs"]["p999"]["all"]["quantilePopulationCount"]
        return player_count
    
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
        return(best_keys)
    
    @staticmethod
    def get_rankings_page(page, season, region):
        api_response = RaiderApi.get_rankings_page(page, season, region)
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
    def get_dungeons():
        api_response = RaiderApi.get_expansion_dungeon_data()
        seasons = api_response['seasons']
        dungeons_json = next(season for season in seasons if season['slug'])['dungeons']
        dungeon_map = RaiderService._create_dungeon_map(dungeons_json)
        return dungeon_map
    
    @staticmethod
    def _create_dungeon_map(dungeons_json):
        dungeon_map = {}
        for entry in dungeons_json:
            dungeon = Dungeon(entry['id'], entry['slug'], entry['name'], entry['short_name'])
            dungeon_map[dungeon.id] = dungeon
        return dungeon_map