import asyncio
import logging

from config import CURRENT_SEASON, get_config
from models.regions import Region
from service.snapshot import SnapshotService


async def main():
    ss_service = SnapshotService()
    ss_service.generate_new_snapshot(Region.US, get_config().get(CURRENT_SEASON), cap=80)

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    asyncio.run(main())
