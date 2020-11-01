import logging
from datetime import datetime
from pathlib import Path

DIR_LOGS = "logs"
FILE_PATH_LOG = f"{DIR_LOGS}/main-{datetime.today().strftime('%Y-%m-%d')}.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

Path(DIR_LOGS).mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s: %(funcName)s]: %(message)s")
file_handler = logging.FileHandler(FILE_PATH_LOG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
