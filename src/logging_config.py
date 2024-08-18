import logging
import logging.config
from functools import wraps

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s]  %(name)s | %(levelname)s | %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": "logs/latest.log",
            "backupCount": 3,
            "maxBytes": 5000000
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f'Calling function: {func.__name__}')
        result = func(*args, **kwargs)
        logger.debug(f'Function {func.__name__} finished')
        return result
    return wrapper