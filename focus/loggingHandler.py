import os
import logging

APP_NAME = "Focus App"
ORG_NAME = "Princess Software Solutions"
log_dir = os.path.join(os.getenv("LOCALAPPDATA"), ORG_NAME, APP_NAME, "logs")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "focus.log")

# Set up the logger
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

# Clear existing handlers to avoid duplicates
logger.handlers.clear()

# File handler (writes to file immediately)
file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Optional: Console output too
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Logging functions
def log_debug(msg): logger.debug(msg)
def log_info(msg): logger.info(msg)
def log_warning(msg): logger.warning(msg)
def log_error(msg): logger.error(msg)
def log_critical(msg): logger.critical(msg)
def log_exception(msg): logger.exception(msg)
