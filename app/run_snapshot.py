import logging
from config import CURRENT_SEASON, get_config
from service.snapshot import SnapshotService


def main():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger("run_snapshot")
    logger.info("Starting M+ snapshot generation job")

    season = get_config().get(CURRENT_SEASON)
    logger.info(f"Target season: {season}")

    ss_service = SnapshotService()
    ss_service.generate_snapshot_all_regions(season)

    logger.info("Snapshot generation job finished successfully")


if __name__ == "__main__":
    main()
