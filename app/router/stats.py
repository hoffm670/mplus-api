from fastapi import APIRouter
from service.snapshot import SnapshotService




class StatsRouter(APIRouter):
    
    def __init__(self):
        super().__init__(prefix="/stats")
        self.ss_service = SnapshotService()
    
        @self.get("")
        async def get_mplus_stats():
            return self.ss_service.get_latest_snapshot()

        @self.post("/refresh")
        async def refresh_mplus_stats():
            return self.ss_service.generate_new_snapshot()