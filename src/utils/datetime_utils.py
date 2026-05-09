from datetime import datetime
from zoneinfo import ZoneInfo
from src.constants import Constants


class DateTimeUtils():
    TIMEZONE = Constants.SYSTEM_TIME_ZONE

    @classmethod
    def get_current_day_name(cls):
        return datetime.now(ZoneInfo(cls.TIMEZONE)).strftime("%A").lower()
