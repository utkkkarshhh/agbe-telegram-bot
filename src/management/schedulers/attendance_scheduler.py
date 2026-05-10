import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from src.constants import OdooConstants
from src.managers import OdooManager
from src.telegram import TelegramManager, TelegramUserManager
from src.utils import DateTimeUtils, logger


class AttendanceScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=DateTimeUtils.TIMEZONE)
        self.odoo_manager = (OdooManager())

    def start(self):
        logger.info("Registering attendance cron jobs")
        if not OdooConstants.IS_AUTO_ATTENDANCE_ENABLED:
            logger.warning("Auto attendance is disabled")
            return

        checkin_hour, checkin_minute = DateTimeUtils.parse_time_string(OdooConstants.AUTO_CHECK_IN_TIME)
        checkout_hour, checkout_minute = DateTimeUtils.parse_time_string(OdooConstants.AUTO_CHECK_OUT_TIME)

        logger.info(f"Auto check-in scheduled at {checkin_hour}:{checkin_minute}")
        logger.info(f"Auto check-out scheduled at {checkout_hour}:{checkout_minute}")

        self.scheduler.add_job(func=self.auto_checkin,
                               trigger="cron",
                               hour=checkin_hour,
                               minute=checkin_minute)

        self.scheduler.add_job(func=self.auto_checkout,
                               trigger="cron",
                               hour=checkout_hour,
                               minute=checkout_minute)
        self.scheduler.start()

    def auto_checkin(self):
        try:
            if self.is_off_day():
                return
            logger.info("Starting auto check-in")
            self.odoo_manager.authenticate()
            response = self.odoo_manager.check_in()
            logger.info(response)
            self.send_telegram_message(response)
        except Exception as e:
            logger.exception(f"Auto check-in failed: {e}")

    def auto_checkout(self):
        try:
            if self.is_off_day():
                return
            logger.info("Starting auto check-out")
            self.odoo_manager.authenticate()
            response = self.odoo_manager.check_out()
            logger.info(response)
            self.send_telegram_message(response)
        except Exception as e:
            logger.exception(f"Auto check-out failed: {e}")

    def is_off_day(self) -> bool:
        current_day = DateTimeUtils.get_current_day_name()
        if current_day in OdooConstants.OFF_DAYS:
            logger.info(
                f"OK - {current_day} is an off day. "
                f"Skipping attendance action"
            )
            return True
        return False

    def send_telegram_message(self, message: str):
        users = TelegramUserManager.get_all_users()
        if not users:
            logger.warning("No telegram users registered")
            return
        user = users[0]
        try:
            asyncio.run(TelegramManager.send_message(chat_id=user["chat_id"], message=message))
        except Exception as e:
            logger.exception(f"Failed sending telegram " f"message: {e}")
