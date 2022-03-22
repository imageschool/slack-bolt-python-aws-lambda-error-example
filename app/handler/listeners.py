import logging

from slack_bolt.app.async_app import AsyncApp

from app.handler.message import message_status, message_magic
from config import STR_LOGGER_NAME

logger = logging.getLogger(STR_LOGGER_NAME)


async def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        logger.debug(f":x: Usage: /start-process (magic)")
        await ack(f":x: Usage: /start-process (magic)")
    else:
        logger.debug(f"Accepted! (task: {body['text']})")
        await ack(f"Accepted! (task: {body['text']})")


def register_listeners(app: AsyncApp):
    # Messages
    app.message("status")(message_status)
    app.message("magic")(
        ack=respond_to_slack_within_3_seconds,
        lazy=[message_magic]
    )
