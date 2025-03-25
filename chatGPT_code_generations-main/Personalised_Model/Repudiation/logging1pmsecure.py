#create a secure python logger for a program
import logging
import logging.handlers
import os

# Secure log file path
LOG_FILE = "secure_app.log"

# Ensure log file has secure permissions (Linux/macOS)
if os.path.exists(LOG_FILE):
    os.chmod(LOG_FILE, 0o600)  # Read & write only for the owner

# Formatter to standardize log output
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_secure_logger(name="SecureLogger"):
    """Creates and returns a secure logger instance."""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Adjust logging level as needed

    # Prevent duplicate log handlers
    if logger.hasHandlers():
        return logger

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Secure Rotating File Handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5  # 5MB per log file, keeps last 5
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Secure Permissions (Windows alternative)
    try:
        os.chmod(LOG_FILE, 0o600)  # Apply file permission again (in case of new file creation)
    except PermissionError:
        pass  # Handle cases where chmod is restricted

    # Add Handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Example usage
logger = get_secure_logger()
logger.info("Secure logger initialized successfully.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")

#does have a max limit plus backups.
#permissions
