from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from src.utils import logger

class AttendanceScheduler:

    def __init__(self):
        self.scheduler = (BackgroundScheduler())

    def start(self):
        logger.info("Registering scheduler jobs")
        self.scheduler.add_job(
            func=self.print_hello,
            trigger="interval",
            seconds=5
        )
        self.scheduler.start()
        logger.info("Attendance scheduler started")

    def print_hello(self):

        logger.info("Hello")
