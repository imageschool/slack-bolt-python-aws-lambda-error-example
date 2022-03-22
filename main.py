import logging
import os
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import router
from app.handler.listeners import register_listeners
from config import LogConfig, STR_LOGGER_NAME, SLACK_SIGNING_SECRET, SLACK_BOT_TOKEN

# Logger
dictConfig(LogConfig().dict())
logger = logging.getLogger(STR_LOGGER_NAME)
logger.info('logger enabled.')

# Environment
current_env = os.getenv('ENVIRONMENT')
logger.info(f"current env={current_env}")

# FastAPI
app = FastAPI(
    title='slack-lambda-test',
    root_path=''
)

PREFIX_DEFAULT = '/api/v1'
app.include_router(router, prefix=PREFIX_DEFAULT)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if os.getenv('ENVIRONMENT') == 'local':
    # Uvicorn running for easy debugging purpose in local env
    uvicorn.run(app=app, host='0.0.0.0', port=8080)
else:
    logger.info('Setting Bolt-Python AWS Lambda handler')
    slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET, process_before_response=True)

    # Registering all listeners for slack-bolt
    register_listeners(app=slack_app)


# AWS Lambda handler
def handler(event, context):
    app_handler = SlackRequestHandler(app=slack_app)
    return app_handler.handle(event, context)
