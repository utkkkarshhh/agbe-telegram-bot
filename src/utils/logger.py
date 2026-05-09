import logging
from src.constants import Constants

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
    }
    RESET = "\033[0m"
    def format(self, record):
        log_color = self.COLORS.get(
            record.levelname,
            self.RESET
        )
        formatted_message = super().format(record)
        return (
            f"{log_color}"
            f"{formatted_message}"
            f"{self.RESET}"
        )

logger = logging.getLogger(Constants.BOT_NAME)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
formatter = ColoredFormatter(
    fmt=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
