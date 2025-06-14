import os, sys
from pathlib import Path


# Logic to get the proper directory regardless of exe or py
if getattr(sys, 'frozen', False):
    cwd = Path(sys.argv[0]).resolve().parent
else:
    cwd = Path(__file__).resolve().parent.parent

log_dir = os.path.join(cwd, 'logs')

if not os.path.exists(log_dir):
    print("Building log directory")
    os.makedirs(log_dir)

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
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": f"{log_dir}/latest.log",
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

