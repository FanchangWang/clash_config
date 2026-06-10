import logging
import sys


def get_logger(name: str = "clash_config") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(stream=sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
    return logger


logger = get_logger()

logging.getLogger("httpx").setLevel(logging.WARNING)
