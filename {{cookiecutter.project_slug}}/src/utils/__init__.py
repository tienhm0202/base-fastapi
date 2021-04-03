import logging

from zogutils.middlewares import logger
from zogutils.secret import unique_id


def get_db_id() -> str:
    return unique_id(16, "ID_")


def get_secret() -> str:
    return unique_id(32, "KEY_")


def get_logger(name: str):
    level = logging.getLevelName(settings.LOG_LEVEL)

    new_logger = logger.get_logger(name)
    new_logger.setLevel(level)

    return new_logger
