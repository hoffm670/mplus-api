from fastapi import APIRouter, HTTPException
from service.snapshot import SnapshotService
from service.config import ConfigService


class StatsRouter(APIRouter):

    def __init__(self):
        super().__init__(prefix="/stats")
        self.ss_service = SnapshotService()
        self.config_service = ConfigService()

        @self.get("")
        async def get_mplus_stats(region: str):
            return self.ss_service.get_latest_snapshot(region)

        @self.post("/refresh")
        async def refresh_mplus_stats():
            if self.config_service.config.get("refresh-enabled", False) == "true":
                return self.ss_service.generate_snapshot_all_regions()
            else:
                raise HTTPException(status_code=404)
