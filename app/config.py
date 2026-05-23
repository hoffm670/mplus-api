import os

# VARIABLES
REFRESH_ENDPOINT_TOGGLE = "refresh-endpoint-toggle"
CURRENT_SEASON = "current-season"
CURRENT_EXPANSION_ID = "current-expansion-id"
COLLECTION_PREFIX = "collection-prefix"
RANKINGS_MAX_RETRIES = "rankings-max-retries"
RANKINGS_RETRY_BACKOFF_SECONDS = "rankings-retry-backoff-seconds"

DEV_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: True,
    CURRENT_SEASON: "season-mn-1",
    CURRENT_EXPANSION_ID: "11",
    COLLECTION_PREFIX: "snapshot-dev",
    RANKINGS_MAX_RETRIES: 3,
    RANKINGS_RETRY_BACKOFF_SECONDS: 0.5,
}

PROD_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: False,
    CURRENT_SEASON: "season-mn-1",
    CURRENT_EXPANSION_ID: "11",
    COLLECTION_PREFIX: "snapshot",
    RANKINGS_MAX_RETRIES: 3,
    RANKINGS_RETRY_BACKOFF_SECONDS: 0.5,
}


def get_config():
    if os.environ.get('ENVIRONMENT', 'DEV') == 'PROD':
        return PROD_CONFIG
    else:
        return DEV_CONFIG


def get_collection_for_tier(tier: str) -> str:
    return f"{get_config().get(COLLECTION_PREFIX)}-{tier}"
