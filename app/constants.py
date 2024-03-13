# Affixes
FORT = 'Fortified'
FORT_ID = 10
TYRAN = 'Tyrannical'
TYRAN_ID = 9

AFFIX_MAP = {
    TYRAN_ID: TYRAN,
    FORT_ID: FORT
}


# API
SEASON_CUTOFF = 'https://raider.io/api/v1/mythic-plus/season-cutoffs'
GET_CHARACTER = 'https://raider.io/api/v1/characters/profile'
GET_STATIC_DATA = 'https://raider.io/api/v1/mythic-plus/static-data?expansion_id=9'  # TODO make expansion id not static

GET_RANKINGS_PAGE = 'https://raider.io/api/mythic-plus/rankings/characters'
PAGE_SIZE = 40

GET_CHARACTER_FIELDS = 'mythic_plus_best_runs,mythic_plus_alternate_runs'

# Database
SNAPSHOTS = 'snapshot'
TIMESTAMP = 'timestamp'
REGION = 'region'
