import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from core.logging import InterceptHandler

VERSION = "0.0.1"
API_PREFIX = "/api"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL, default="mysql://root:root@localhost/fastapi")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example application")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)

# Template dir
TEMPLATE_DIR = config('TEMPLATE_DIR', default='templates')

# Openai Chatgpt
BOT_DESC = config('BOT_DESC', default="You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.")
API_KEY= config('API_KEY', default="")
MODEL="gpt-3.5-turbo"

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

# intercept standard logging messages toward your Loguru sinks
logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

