#create a secure python logger for a program
import logging
import logging.handlers
import os
import re

# Define a pattern for sensitive data (e.g., passwords, API keys)
SENSITIVE_DATA_PATTERNS = [
    (re.compile(r"(password\s*=\s*)\S+", re.IGNORECASE), r"\1[REDACTED]"),
    (re.compile(r"(api_key\s*=\s*)\S+", re.IGNORECASE), r"\1[REDACTED]"),
]

class RedactingFilter(logging.Filter):
    """Filter to redact sensitive data in logs."""

    def filter(self, record):
        record.msg = self.redact(record.getMessage())
        return True

    def redact(self, message):
        for pattern, replacement in SENSITIVE_DATA_PATTERNS:
            message = pattern.sub(replacement, message)
        return message

def get_secure_logger(name="SecureLogger", log_file="secure_app.log"):
    """Creates a secure logger with log rotation and sensitive data filtering."""
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create a rotating file handler (max 5MB per file, keeping 3 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, log_file), maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setLevel(logging.INFO)

    # Set file permissions (only user can read/write)
    log_path = os.path.join(log_dir, log_file)
    os.chmod(log_path, 0o600)  # Only owner can read/write

    # Define log format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(log_format)

    # Apply the redacting filter
    file_handler.addFilter(RedactingFilter())

    # Add handler to logger
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger

# Example Usage
logger = get_secure_logger()

logger.info("User login attempt successful")
logger.warning("password=supersecret123")  # This will be redacted
logger.error("api_key=abcdef123456")  # This will be redacted


#bad
#does not redact all info, info disclosure
#can fail permissions, therefore no access control
#log messages could be altered
#log inection attacks
