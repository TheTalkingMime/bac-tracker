import time
from logging_config import LOGGING_CONFIG
import logging
from functools import wraps

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def retry_on_exception(exception_type, retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            n = 0
            while n < retries:
                try:
                    return func(*args, **kwargs)
                except exception_type as e:
                    n += 1
                    args_str = ", ".join(map(str, args))
                    kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
                    logger.warning(f"{func.__name__}({args_str}, {kwargs_str}) failed on attempt # {n}")
                    time.sleep(delay)
                    if n >= retries:
                        logger.error(f"Failed after {retries} retries with {delay} second delay. Error: {e}")
                        raise
        return wrapper
    return decorator