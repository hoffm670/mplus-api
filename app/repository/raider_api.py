import logging
import time

import requests
from urllib.parse import urljoin, urlencode

from config import (
    get_config,
    CURRENT_EXPANSION_ID,
    RANKINGS_MAX_RETRIES,
    RANKINGS_RETRY_BACKOFF_SECONDS,
)
from constants import (GET_CHARACTER, GET_CHARACTER_FIELDS, GET_RANKINGS_PAGE,
                       GET_STATIC_DATA, SEASON_CUTOFF)

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

    @staticmethod
    def get_rankings_page(page, season, region):
        params = {
            "region": region,
            "season": season,
            "class": "all",
            "role": "all",
            "page": page,
        }

        config = get_config()
        max_retries = int(config.get(RANKINGS_MAX_RETRIES, 3))
        backoff_seconds = float(config.get(RANKINGS_RETRY_BACKOFF_SECONDS, 0.5))

        last_exception = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(GET_RANKINGS_PAGE, params=params)
            except requests.RequestException as exc:
                last_exception = exc
                logger.warning(
                    f'Exception retrieving rankings page {page} - {season} - {region} '
                    f'(attempt {attempt}/{max_retries}): {exc}'
                )
            else:
                if response.status_code == 200:
                    logger.debug(f'Retreived rankings page {page} - {season} - {region}')
                    return response.json()

                logger.warning(
                    f'Failed to retreive rankings page {page} - {season} - {region} '
                    f'(attempt {attempt}/{max_retries}): '
                    f'{response.status_code} - {response.reason}'
                )

            if attempt < max_retries:
                time.sleep(backoff_seconds * attempt)

        logger.error(
            f'Exhausted retries retrieving rankings page {page} - {season} - {region}'
        )
        if last_exception:
            raise last_exception
        raise RuntimeError(
            f'Failed to retreive rankings page {page} - {season} - {region} '
            f'after {max_retries} attempts'
        )

    @staticmethod
    def get_expansion_dungeon_data():
        params = {'expansion_id': get_config().get(CURRENT_EXPANSION_ID)}
        response = requests.get(urljoin(GET_STATIC_DATA,  "?" + urlencode(params)))
        if response.status_code == 200:
            logger.debug('Retreived expansion dungeon static data')
            return response.json()
        else:
            logger.error(
                f'Failed to retreive expansion dungeon static data. {response.status_code} - {response.reason}')
