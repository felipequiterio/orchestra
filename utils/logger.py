import logging
import inspect
from colorama import init, Fore, Style
from pathlib import Path

init(autoreset=True)


class CustomFormatter(logging.Formatter):
    LOG_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        # Get the original formatted message
        formatted_msg = super().format(record)

        try:
            # Get the file path from record
            file_path = Path(record.pathname)

            # Try to make it relative if it's in our project
            try:
                relative_path = file_path.relative_to(Path.cwd())
                location = f"{relative_path}:{record.lineno}"
            except ValueError:
                # For system files, just use filename
                location = f"{file_path.name}:{record.lineno}"

            # Return formatted message with location
            return f"{location} - {formatted_msg}"

        except Exception:
            # Fallback to just the message if anything goes wrong
            return formatted_msg


def get_custom_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = CustomFormatter()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Optional: File Handler for persistent logging
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Optional: Add a function to log exceptions with full traceback
def log_exception(logger, message, exc_info=True):
    """
    Helper function to log exceptions with full traceback
    """
    logger.error(message, exc_info=exc_info)
