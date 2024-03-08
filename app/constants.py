# Regions
REGION_US = 'us'

# Affixes
FORT = 'Fortified'
FORT_ID = 10
TYRAN = 'Tyrannical'
TYRAN_ID = 9

AFFIX_MAP = {
    TYRAN_ID: TYRAN,
    FORT_ID: FORT
}

# Season 3
DF_S3 = 'season-df-3'
CURRENT_SEASON = DF_S3  # TODO have a config file

BRH = 'BRH'
AD = 'AD'
FALL = 'FALL'
DHT = 'DHT'
WM = 'WM'
EB = 'EB'
RISE = 'RISE'
TOTT = 'TOTT'
DF_S3_DUNGEONS = [BRH, AD, FALL, DHT, WM, EB, RISE, TOTT]


# API
SEASON_CUTOFF = 'https://raider.io/api/v1/mythic-plus/season-cutoffs'
GET_CHARACTER = 'https://raider.io/api/v1/characters/profile'
GET_STATIC_DATA = 'https://raider.io/api/v1/mythic-plus/static-data?expansion_id=9'  # TODO make expansion id not static
GET_RANKINGS_PAGE = 'https://raider.io/api/mythic-plus/rankings/characters'

GET_CHARACTER_FIELDS = 'mythic_plus_best_runs,mythic_plus_alternate_runs'

# Scraper
RAIDER_RANKINGS_URL = 'https://raider.io/mythic-plus-character-rankings'
PAGE_SIZE = 40

ROW_CLASS = 'mythic-plus-rankings--row'

CHARACTER_SELECTOR = 'td:nth-child(2) > div > div > span'
SERVER_SELECTOR = 'td:nth-child(2) > div > div > div'

SERVER_REGEX = r"^\((\w{2})\)\s(.+)$"
