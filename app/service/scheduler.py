import asyncio
import logging
from datetime import date, datetime

from config import CURRENT_SEASON, get_config
from service.snapshot import SnapshotService

logger = logging.getLogger(__name__)


class DailyScheduler:
    """Lightweight asyncio scheduler replacing Rocketry."""

    def __init__(self, start_hour: int = 8, end_hour: int = 14, poll_seconds: int = 60):
        self._start_hour = start_hour
        self._end_hour = end_hour
        self._poll_seconds = poll_seconds
        self._stop_event = asyncio.Event()
        self._last_run_date: date | None = None
        self._ss_service = SnapshotService()

    def shut_down(self) -> None:
        self._stop_event.set()

    async def serve(self) -> None:
        while not self._stop_event.is_set():
            now = datetime.now()
            if (
                self._start_hour <= now.hour < self._end_hour
                and self._last_run_date != now.date()
            ):
                self._last_run_date = now.date()
                logger.info("Starting scheduled snapshot")
                await asyncio.to_thread(
                    self._ss_service.generate_snapshot_all_regions,
                    get_config().get(CURRENT_SEASON),
                )

            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=self._poll_seconds)
            except asyncio.TimeoutError:
                pass


scheduler = DailyScheduler()
