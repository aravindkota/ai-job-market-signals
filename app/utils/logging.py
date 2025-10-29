"""PURPOSE: Structured logging setup and helpers.
"""


import logging

# PURPOSE: Configure simple structured logging; replace with loguru or structlog if preferred.
def get_logger(name: str = "app"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
