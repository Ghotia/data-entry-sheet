import logging
import json
from logging.handlers import RotatingFileHandler

LOG_PATH = 'phishing_detector/detections.log'

logger = logging.getLogger('phishing_detector')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = RotatingFileHandler(LOG_PATH, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_detection(item: dict):
    # Write a JSON line for auditing
    logger.info(json.dumps(item))
