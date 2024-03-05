import logging

import requests
from constants import GET_CHARACTER, GET_CHARACTER_FIELDS, SEASON_CUTOFF

logger = logging.getLogger('raider.api')


class RaiderApi:

    @staticmethod
    def get_season_cutoff(season, region):
        params = {"season": season, "region": region}
        response = requests.get(SEASON_CUTOFF, params=params)
        if response.status_code == 200:
            logger.debug('Retreived mplus cutoff info')
            return response.json()
        else:
            logger.error(
                f'Failed to retrieve mplus cutoff info. {response.status_code} - {response.reason}')

    @staticmethod
    def get_character_profile(name, realm, region):
        params = {"name": name, "realm": realm,
                  "region": region, "fields": GET_CHARACTER_FIELDS}
        response = requests.get(GET_CHARACTER, params=params)
        if response.status_code == 200:
            logger.debug(
                'Retreived character info for {name} - {realm} - {region}')
            return response.json()
        else:
            logger.error(
                f'Failed to retrieve character info for {name} - {realm} - {region}.')
            logger.error(f'Error: {response.status_code} - {response.reason}')
