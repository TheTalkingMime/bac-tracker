import time
from logging_config import LOGGING_CONFIG
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def retry_on_exception(func, exception_type, retries=3, delay=1):
    n = 0
    try:
        return func()
    except exception_type as e:
        n += 1
        if n >= retries:
            logger.error(f"Exception occurred {n} times in a row: \n{e}")
            raise
        logger.warning(f"Exception occurred: {e}. Retrying in {delay} seconds...")
        time.sleep(delay)