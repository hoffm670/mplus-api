import os

# VARIABLES
REFRESH_ENDPOINT_TOGGLE = "refresh-endpoint-toggle"
CURRENT_SEASON = "current-season"
CURRENT_EXPANSION_ID = "current-expansion-id"
IS_PROD = "is_prod"


DEV_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: True,
    CURRENT_SEASON: "season-tww-1",
    CURRENT_EXPANSION_ID: "10",
    IS_PROD: "false"

}

PROD_CONFIG = {
    REFRESH_ENDPOINT_TOGGLE: False,
    CURRENT_SEASON: "season-tww-1",
    CURRENT_EXPANSION_ID: "10",
    IS_PROD: "true"
}


def get_config():
    if os.environ.get('ENVIRONMENT', 'DEV') == 'PROD':
        return PROD_CONFIG
    else:
        return DEV_CONFIG
