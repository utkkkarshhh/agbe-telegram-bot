from typing import Tuple

from datetime import datetime, time
from zoneinfo import ZoneInfo
from src.constants import Constants


class DateTimeUtils():
    TIMEZONE = Constants.SYSTEM_TIME_ZONE

    @classmethod
    def get_current_day_name(cls):
        return datetime.now(ZoneInfo(cls.TIMEZONE)).strftime("%A").lower()

    @classmethod
    def parse_time_string(cls, time_str: str) -> Tuple[int, int]:
        try:
            dt = datetime.strptime(time_str, "%H:%M")
            return dt.hour, dt.minute
        except ValueError:
            return 9, 0
