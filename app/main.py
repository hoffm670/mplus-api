import asyncio

import uvicorn
from router import api_app
from constants import DF_S3, REGION_US, FORT, TYRAN
from service.scraper import app as app_rocketry
import logging

from repository.firestore import FirestoreRepository
from service.snapshot import SnapshotService
from service.raider import RaiderService


class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run Rocketry and FastAPI"

    server = Server(config=uvicorn.Config(api_app, host='0.0.0.0', port=8080, workers=1, loop="asyncio", log_config="log_conf.yaml"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    # Print Rocketry's logs to terminal
    # Run both applications
    asyncio.run(main())


# if __name__ == "__main__":
#     config = uvicorn.Config("main:app", port=8080, log_level="info", log_config="log_conf.yaml")
#     server = uvicorn.Server(config)
#     server.run()