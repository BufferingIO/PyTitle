import logging
import os


def get_logger(name: str) -> logging.Logger:
    formatter = logging.Formatter(fmt="%(name)s %(levelname)s: %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(os.getenv("LOG_LEVEL", "info").upper())
    logger.addHandler(handler)
    return logger
