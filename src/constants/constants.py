import os
from dotenv import load_dotenv

load_dotenv()

class Constants:
    BOT_NAME = os.getenv("BOT_NAME")
    SYSTEM_TIME_ZONE=os.getenv("SYSTEM_TIME_ZONE", "Asia/Kolkata")
    TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

class OdooConstants:
    ODOO_URL = os.getenv("ODOO_URL")
    ODD_DB = os.getenv("ODD_DB")
    ODOO_USERNAME = os.getenv("ODOO_USERNAME")
    ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")
    WORK_FROM_OFFICE_DAYS = ["monday", "tuesday", "wednesday"]
    WORK_FROM_HOME_DAYS = ["thursday", "friday"]
    OFF_DAYS = ["saturday", "sunday"]
    IS_AUTO_ATTENDANCE_ENABLED = os.getenv("IS_AUTO_ATTENDANCE_ENABLED", "False").lower() == "true"
    AUTO_CHECK_IN_TIME = os.getenv("AUTO_CHECK_IN_TIME", "9:00")
    AUTO_CHECK_OUT_TIME = os.getenv("AUTO_CHECK_OUT_TIME", "18:00")
    AGBE_COORDINATES = {
        "lat": 28.4018581,
        "long": 77.0477487
    }
    HOME_COORDINATES = {
        "lat": 28.6809867,
        "long": 76.9321791
    }
