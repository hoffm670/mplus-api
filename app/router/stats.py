from fastapi import APIRouter, HTTPException, BackgroundTasks
from service.snapshot import SnapshotService
from config import get_config, REFRESH_ENDPOINT_TOGGLE, CURRENT_SEASON


class StatsRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/stats")
        self.ss_service = SnapshotService()

        @self.get("")
        async def get_mplus_stats(region: str):
            return self.ss_service.get_latest_snapshot(region)

        @self.post("/refresh")
        async def refresh_mplus_stats(background_tasks: BackgroundTasks):
            if get_config().get(REFRESH_ENDPOINT_TOGGLE, False):
                background_tasks.add_task(self.ss_service.generate_snapshot_all_regions, get_config().get(CURRENT_SEASON))
                return {"message": "Refresh started."}
            else:
                raise HTTPException(status_code=404)
