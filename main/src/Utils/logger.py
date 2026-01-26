import logging
import os

# Ensure logs directory exists
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, 'user_changes.log')

# Setup logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def log_change(user_id, field, old_value, new_value):
    logger.info(f"User ID: {user_id} updated {field}. Old: '{old_value}' -> New: '{new_value}'")
