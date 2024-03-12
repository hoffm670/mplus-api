import logging

from rocketry import Rocketry
from service.snapshot import SnapshotService

app = Rocketry(config={"task_execution": "async"})

logger = logging.getLogger(__name__)

ss_service = SnapshotService()


@app.task('daily between 08:00 and 14:00')
def run_refresh():
    logger.info('Starting scheduled snapshot')
    ss_service.generate_snapshot_all_regions()
