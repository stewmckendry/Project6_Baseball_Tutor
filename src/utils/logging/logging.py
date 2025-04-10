import logging
import os

def setup_logger(name="socratic_coach"):
    logger = logging.getLogger(name)
    if logger.handlers:  # Prevent duplicate logs
        return logger

    logger.setLevel(logging.DEBUG)

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
