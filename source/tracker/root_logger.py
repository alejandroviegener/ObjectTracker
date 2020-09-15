
import logging

# Define parrent logger name
LOGGER_NAME = "tracker"

# Define log parent
logger = logging.getLogger(LOGGER_NAME)

# Set defaul level
logger.setLevel(logging.WARNING)

# Stream handler
stream_handler = logging.StreamHandler()

# Default formatter
formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")

# Add formatter to hadler
stream_handler.setFormatter(formatter)

# Set handler to logger
logger.addHandler(stream_handler)

# Utils function
def add_file_handler(file):
    """Adds a log file handler to the logger"""
    file_handler = logging.FileHandler(file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

