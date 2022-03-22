import logging
import random
import sys
import time
from datetime import datetime

import requests
from slack_bolt.context.say.async_say import AsyncSay

from config import STR_LOGGER_NAME

STR_SOMETHING_WENT_WRONG = "STR_SOMETHING_WENT_WRONG"
STR_READ_TIMEOUT = "STR_READ_TIMEOUT"

logger = logging.getLogger(STR_LOGGER_NAME)


def get_requests():
    random_time = random.uniform(0.1, 0.6)
    time.sleep(random_time)
    return f"some_result {random_time}"


async def message_magic(message: dict, say: AsyncSay):
    logger.debug('message MAGIC magic')

    try:
        logger.info("Get Requests")
        res, res2, res3 = get_requests(), get_requests(), get_requests()
        logger.info("Responses arrived")

        dt = datetime.today().strftime("%H:%M:%S, %d/%m/%Y")
        await say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Some Status*:"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "text": f"*{dt}* | {res}, {res2}, {res3}",
                            "type": "mrkdwn"
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ],
            text='msg'
        )

        logger.info('say() done')
    except requests.exceptions.ReadTimeout as e:
        logger.info(message['user'])
        logger.error(e)
    except Exception as e:
        logger.info(message['user'])
        logger.error(e)
    except:
        logger.info(message['user'])
        logger.error("Unexpected error:", sys.exc_info()[0])
        raise


async def message_status(message: dict, say: AsyncSay):
    logger.debug('message status')

    try:
        logger.info("Get Requests")
        res, res2, res3 = get_requests(), get_requests(), get_requests()
        logger.info("Responses arrived")

        dt = datetime.today().strftime("%H:%M:%S, %d/%m/%Y")
        await say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Some Status*:"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "text": f"*{dt}* | {res}, {res2}, {res3}",
                            "type": "mrkdwn"
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ],
            text='msg'
        )
    except requests.exceptions.ReadTimeout as e:
        logger.info(message['user'])
        logger.error(e)

    except Exception as e:
        logger.info(message['user'])
        logger.error(e)
