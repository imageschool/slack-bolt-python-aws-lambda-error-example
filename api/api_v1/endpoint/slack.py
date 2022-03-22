import logging

from fastapi import APIRouter, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from starlette import status

from app.handler.listeners import register_listeners
from config import STR_LOGGER_NAME, SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET

"""
    Used in local environment to debug
"""

PREFIX_SLACK = '/slack'
logger = logging.getLogger(STR_LOGGER_NAME)
router = APIRouter(prefix=PREFIX_SLACK)

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

register_listeners(app=app)

app_handler = SlackRequestHandler(app=app)


@router.get('', status_code=status.HTTP_200_OK)
def hello_slack():
    return {
        'Hello': 'Slack'
    }


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
