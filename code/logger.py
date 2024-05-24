import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(os.path.join(log_dir, 'blackboard.log'), maxBytes=10000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('blackboard')  # Ensure a consistent logger name
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

logger = setup_logger('log')
