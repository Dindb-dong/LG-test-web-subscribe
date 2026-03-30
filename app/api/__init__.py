"""API router aggregation for the webOS dashboard."""

from fastapi import APIRouter

from app.api.v1.devices import router as devices_router
from app.api.v1.subscribers import router as subscribers_router

api_router = APIRouter()
api_router.include_router(subscribers_router)
api_router.include_router(devices_router)
