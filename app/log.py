import logging
import os

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Also print to console
    ]
)

logger = logging.getLogger("SmartEmailAssistant")
