from fastapi import FastAPI
from .health import router as health_router
from .stats import StatsRouter

api_app = FastAPI()
api_app.include_router(health_router)
api_app.include_router(StatsRouter())
