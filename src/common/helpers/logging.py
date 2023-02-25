import structlog
from logging import Logger


def get_logger(logger_name: str) -> Logger:
    logger: Logger = structlog.get_logger(logger_name)
    return logger
