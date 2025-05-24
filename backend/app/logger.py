import logging
import os

def setup_logger():
    logger = logging.getLogger("backend_logger")
    logger.setLevel(logging.DEBUG)

    log_dir = "/var/log/backend"
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(f"{log_dir}/app.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger
