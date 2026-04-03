import os

# VARIABLES
REFRESH_ENDPOINT_TOGGLE = "refresh-endpoint-toggle"
CURRENT_SEASON = "current-season"
CURRENT_EXPANSION_ID = "current-expansion-id"
COLLECTION = "collection"
RANKINGS_MAX_RETRIES = "rankings-max-retries"
RANKINGS_RETRY_BACKOFF_SECONDS = "rankings-retry-backoff-seconds"

DEV_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: True,
    CURRENT_SEASON: "season-mn-1",
    CURRENT_EXPANSION_ID: "11",
    COLLECTION: "snapshot-dev",
    RANKINGS_MAX_RETRIES: 3,
    RANKINGS_RETRY_BACKOFF_SECONDS: 0.5,
}

PROD_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: False,
    CURRENT_SEASON: "season-mn-1",
    CURRENT_EXPANSION_ID: "11",
    COLLECTION: "snapshot",
    RANKINGS_MAX_RETRIES: 3,
    RANKINGS_RETRY_BACKOFF_SECONDS: 0.5,
}


def get_config():
    if os.environ.get('ENVIRONMENT', 'DEV') == 'PROD':
        return PROD_CONFIG
    else:
        return DEV_CONFIG
