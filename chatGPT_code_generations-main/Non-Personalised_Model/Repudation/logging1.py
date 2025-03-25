#create a python logger for a program
import logging
import os

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
LOG_FILE = "logs/app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Log to file
        logging.StreamHandler()         # Log to console
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Example usage
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error message")
logger.critical("This is a critical error")

#bad
#no file permissions
#check no sesnsitve info is logged
#log injection attackk
#no bounding, identifinte growth.
