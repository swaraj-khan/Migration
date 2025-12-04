import sys
import datetime
from ..config.settings import LOG_LEVEL

COLORS = {
    "INFO": "\033[94m",
    "WARN": "\033[93m",
    "ERROR": "\033[91m",
    "RESET": "\033[0m"
}

LEVELS = ["INFO", "WARN", "ERROR"]
CURRENT_LEVEL_INDEX = LEVELS.index(LOG_LEVEL) if LOG_LEVEL in LEVELS else 0


def log(level: str, message: str):
    if LEVELS.index(level) < CURRENT_LEVEL_INDEX:
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = COLORS.get(level, "")
    reset = COLORS["RESET"]

    sys.stdout.write(f"{color}[{timestamp}] [{level}] {message}{reset}\n")
    sys.stdout.flush()


def info(msg: str):
    log("INFO", msg)


def warn(msg: str):
    log("WARN", msg)


def error(msg: str):
    log("ERROR", msg)
