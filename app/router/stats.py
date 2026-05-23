from fastapi import APIRouter, HTTPException, BackgroundTasks
from constants import TIER_P999, TIERS
from service.snapshot import SnapshotService
from config import get_config, REFRESH_ENDPOINT_TOGGLE, CURRENT_SEASON


class StatsRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/stats")
        self.ss_service = SnapshotService()

        @self.get("")
        async def get_mplus_stats(region: str, tier: str = TIER_P999):
            if tier not in TIERS:
                raise HTTPException(status_code=400, detail=f"tier must be one of {TIERS}")
            return self.ss_service.get_latest_snapshot(region, tier)

        @self.post("/refresh")
        async def refresh_mplus_stats(background_tasks: BackgroundTasks):
            if get_config().get(REFRESH_ENDPOINT_TOGGLE, False):
                background_tasks.add_task(self.ss_service.generate_snapshot_all_regions, get_config().get(CURRENT_SEASON))
                return {"message": "Refresh started."}
            else:
                raise HTTPException(status_code=404)
