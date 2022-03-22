import os

from dotenv import load_dotenv
from pydantic import BaseModel

STR_LOGGER_NAME = 'LOGGER_NAME'


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = STR_LOGGER_NAME
    LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
    LOG_LEVEL: str = 'DEBUG'

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers = {
        LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
    }


if os.getenv('ENVIRONMENT') == 'local':
    load_dotenv('.env.local')
else:
    load_dotenv()

# Slack
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
