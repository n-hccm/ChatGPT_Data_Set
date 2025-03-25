#create a python logger for a program
import logging
import logging.handlers
import os

def setup_logger(log_file="app.log", log_level=logging.INFO):
    """Setup a secure logger with rotating file handler."""
    
    # Create logger
    logger = logging.getLogger("SecureAppLogger")
    logger.setLevel(log_level)
    
    # Prevent adding duplicate handlers
    if logger.hasHandlers():
        return logger

    # Define log format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # File handler with rotation (5MB per file, keeps 3 old logs)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setFormatter(log_format)

    # Console handler for real-time logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Example usage
if __name__ == "__main__":
    logger = setup_logger()
    
    logger.debug("This is a debug message.")
    logger.info("Application started successfully.")
    logger.warning("This is a warning.")
    logger.error("An error occurred!")
    logger.critical("Critical system failure!")

#no permissions
#does have a max limit on space
