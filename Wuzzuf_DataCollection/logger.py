import logging

FILE_PATH_LOG = "logs/main.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s][%(filename)s: %(funcName)s]: %(message)s")
file_handler = logging.FileHandler(FILE_PATH_LOG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)