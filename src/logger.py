import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok = True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
# create a custom logger
logger = logging.getLogger(__name__)
# set the overall logging levvel
logger.setLevel(logging.INFO)

# CREATE a file handlers
file_handler = logging.FileHandler(LOG_FILE_PATH)
console_handler = logging.StreamHandler()
# create formaters and add it to the handlers
formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

#  add handler to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


if __name__ == "__main___":
    logging.info("logging has startted")