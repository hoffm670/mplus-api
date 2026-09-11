import os

# VARIABLES
REFRESH_ENDPOINT_TOGGLE = "refresh-endpoint-toggle"
CURRENT_SEASON = "current-season"
CURRENT_EXPANSION_ID = "current-expansion-id"
COLLECTION_PREFIX = "collection-prefix"
RANKINGS_MAX_RETRIES = "rankings-max-retries"
RANKINGS_RETRY_BACKOFF_SECONDS = "rankings-retry-backoff-seconds"

DEFAULT_SEASON = "season-mn-2"
DEFAULT_EXPANSION_ID = "11"


def get_config():
    is_prod = os.environ.get("ENVIRONMENT", "DEV") == "PROD"
    season = os.environ.get("CURRENT_SEASON") or DEFAULT_SEASON
    expansion_id = os.environ.get("CURRENT_EXPANSION_ID") or DEFAULT_EXPANSION_ID

    return {
        REFRESH_ENDPOINT_TOGGLE: not is_prod,
        CURRENT_SEASON: season,
        CURRENT_EXPANSION_ID: expansion_id,
        COLLECTION_PREFIX: "snapshot" if is_prod else "snapshot-dev",
        RANKINGS_MAX_RETRIES: 3,
        RANKINGS_RETRY_BACKOFF_SECONDS: 0.5,
    }


def get_collection_for_tier(tier: str) -> str:
    return f"{get_config().get(COLLECTION_PREFIX)}-{tier}"
