import asyncio

import uvicorn
from api import api as api_app
from constants import DF_S3, REGION_US
# from app.repository.raider_api import RaiderApi
# from service.raider import RaiderService
from service.scraper import app as app_rocketry


class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run Rocketry and FastAPI"

    server = Server(config=uvicorn.Config(api_app, host='0.0.0.0', port=80, workers=1, loop="asyncio", log_config="log_conf.yaml"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(app_rocketry.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    # Print Rocketry's logs to terminal
    # logger = logging.getLogger("rocketry.task")
    # logger.addHandler(logging.StreamHandler())

    # print(RaiderService.get_cutoff_player_count(DF_S3, REGION_US))
    # print(RaiderService.get_player_highest_keys('kiradh', 'sylvanas', 'eu'))
    # Run both applications
    asyncio.run(main())


# if __name__ == "__main__":
#     config = uvicorn.Config("main:app", port=8080, log_level="info", log_config="log_conf.yaml")
#     server = uvicorn.Server(config)
#     server.run()