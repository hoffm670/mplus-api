import asyncio
from rocketry import Rocketry
from rocketry.conds import every
import logging

app = Rocketry(config={"task_execution": "async"})


logger = logging.getLogger(__name__)

# @app.task(every('10 seconds'))
def run_scraper():
    logger.info('Scheduled task executed')