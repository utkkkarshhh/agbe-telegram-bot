import os

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from src.constants import Constants
from src.management.schedulers import AttendanceScheduler
from src.telegram import TelegramManager
from src.utils import logger

BOT_NAME = Constants.BOT_NAME


def main():
    attendance_scheduler = None
    try:
        logger.info(f"Starting {BOT_NAME}...")
        attendance_scheduler = AttendanceScheduler()
        attendance_scheduler.start()
        logger.info("Attendance scheduler started")
        telegram_manager = TelegramManager()
        logger.info(f"{BOT_NAME} started successfully")
        telegram_manager.run()
        logger.info(f"{BOT_NAME} has been stopped successfully")
    except KeyboardInterrupt:
        logger.warning(f"{BOT_NAME} has been stopped")
    except Exception as error:
        logger.exception(f"{BOT_NAME} stopped unexpectedly: " f"{error}")
    finally:
        if attendance_scheduler:
            attendance_scheduler.scheduler.shutdown(wait=False)
            logger.warning("Attendance scheduler stopped")


if __name__ == "__main__":
    main()
