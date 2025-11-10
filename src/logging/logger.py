import logging
from functools import wraps

def setup_logging():
    """Настройка системы логирования"""
    logging.basicConfig(
        filename='src/logging/shell.log',
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def command_logger(func):
    """Декоратор для логирования команд"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        setup_logging()
        command_name = func.__name__
        try:
            result = func(*args, **kwargs)
            logging.info(f"{command_name}")
            logging.info("SUCCESS")
            return result
        except Exception as e:
            logging.error(f"{command_name}")
            logging.error(f"ERROR: {e}")
            raise
    return wrapper
