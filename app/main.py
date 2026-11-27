import asyncio
import logging

import uvicorn
from service.logging import HealthFilter
from router import api_app
from service.scheduler import scheduler


class Server(uvicorn.Server):
    """Customized uvicorn.Server that shuts down the scheduler on exit."""

    def handle_exit(self, sig: int, frame) -> None:
        scheduler.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    "Run scheduler and FastAPI"

    server = Server(config=uvicorn.Config(api_app, host='0.0.0.0', port=8080, workers=1, loop="asyncio", log_config="log_conf.yaml"))

    api = asyncio.create_task(server.serve())
    sched = asyncio.create_task(scheduler.serve())

    await asyncio.wait([sched, api])

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    logging.getLogger("uvicorn.access").addFilter(HealthFilter())
    asyncio.run(main())
