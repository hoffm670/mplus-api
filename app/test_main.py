import asyncio
import logging

# import uvicorn
from service.logging import HealthFilter
# from router import api_app
# from service.scheduler import app as app_rocketry
from service.snapshot import SnapshotService
from models.regions import Region
from config import get_config, CURRENT_SEASON
from repository.firestore import FirestoreRepository


async def main():
    ss_service = SnapshotService()
    ss_service.generate_new_snapshot(Region.US, get_config().get(CURRENT_SEASON), cap=100)

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    asyncio.run(main())
