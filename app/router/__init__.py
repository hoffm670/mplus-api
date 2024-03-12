from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.health import router as health_router
from router.stats import StatsRouter

api_app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:5000",
    "https://mplus-title-tracker.web.app",
    "https://mplus-title-tracker.web.app/"
]
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_app.include_router(health_router)
api_app.include_router(StatsRouter())
