import logging
import os
from logging.config import dictConfig

import uvicorn
from mangum import Mangum
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import router
from config import LogConfig, STR_LOGGER_NAME

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
    uvicorn.run(app, host='0.0.0.0', port=8080)

logger.info('Setting Mangum handler')
handler = Mangum(app=app)
