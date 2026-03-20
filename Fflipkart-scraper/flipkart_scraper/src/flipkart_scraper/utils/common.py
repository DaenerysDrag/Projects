import logging
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )
