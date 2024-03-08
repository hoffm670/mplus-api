from fastapi import FastAPI
from router.health import router as health_router

api = FastAPI()
api.include_router(health_router)
