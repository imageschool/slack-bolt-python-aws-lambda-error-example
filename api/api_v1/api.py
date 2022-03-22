from fastapi import APIRouter
from api.api_v1.endpoint.slack import router as slack_router

router = APIRouter()
router.include_router(slack_router)
