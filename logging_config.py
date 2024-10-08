import logging
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')

logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL),
    format=LOG_FORMAT,
    stream=logging.StreamHandler()  # Output to stdout
)