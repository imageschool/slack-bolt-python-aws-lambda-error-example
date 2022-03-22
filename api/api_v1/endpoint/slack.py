import logging

from fastapi import APIRouter, Request
from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp
from starlette import status

from app.handler.listeners import register_listeners
from config import STR_LOGGER_NAME, SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

PREFIX_SLACK = '/slack'
logger = logging.getLogger(STR_LOGGER_NAME)
router = APIRouter(prefix=PREFIX_SLACK)

app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET, process_before_response=True)

app_handler = AsyncSlackRequestHandler(app)

# Registering all listeners for slack-bolt
register_listeners(app=app)


@router.post('/events', status_code=status.HTTP_200_OK)
async def endpoint(req: Request):
    # Do not retry (Prevent duplicates)
    if req.headers.get('x-slack-retry-num'):
        return

    logger.debug('Reached /events')
    logger.debug(f"client={req.client}, method = {req.method}, scope = {req.scope}")
    logger.debug(f"scope = {req.scope}")
    return await app_handler.handle(req)


@router.post('/interactive-endpoint', status_code=status.HTTP_200_OK)
async def endpoint(req: Request):
    logger.debug('/interactive-endpoint')
    return await app_handler.handle(req)
