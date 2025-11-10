import logging
from functools import wraps
import sys

def setup_logging():
    """Log config"""
    logging.basicConfig(
        filename='src/logging/shell.log',
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def command_logger(func, ):
    """Decorator for logging commands"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        setup_logging()
        try:
            full_command = " ".join(sys.argv[1:])
            result = func(*args, **kwargs)
            logging.info(f"{full_command}")
            logging.info("SUCCESS")
            return result
        except Exception as e:
            logging.error(f"{full_command}")
            logging.error(f"ERROR: {e}")
            raise
    return wrapper
