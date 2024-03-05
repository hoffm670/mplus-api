from repository.raider_api import RaiderApi
from constants import FORT, TYRAN


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