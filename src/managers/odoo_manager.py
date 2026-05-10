from typing import Dict

import requests
from src.constants import Messages, OdooConstants
from src.utils import DateTimeUtils, logger


class OdooManager:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/148.0.0.0 Safari/537.36"
            )
        }

    def authenticate(self):
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "db": OdooConstants.ODD_DB,
                "login": OdooConstants.ODOO_USERNAME,
                "password": OdooConstants.ODOO_PASSWORD,
            },
        }
        response = self.session.post(
            f"{OdooConstants.ODOO_URL}/web/session/authenticate",
            json=payload,
            headers=self.headers,
        )
        data = response.json()
        if data.get("error"):
            raise Exception(f"Authentication failed: " f"{data['error']}")
        logger.info("Odoo Authentication Successfull")

    def get_coordinates(self) -> Dict:
        if DateTimeUtils.get_current_day_name() in OdooConstants.WORK_FROM_HOME_DAYS:
            return OdooConstants.HOME_COORDINATES
        return OdooConstants.AGBE_COORDINATES

    def get_current_state(self):
        try:
            payload = {"jsonrpc": "2.0", "method": "call", "params": {}, "id": 1}
            response = self.session.post(
                f"{OdooConstants.ODOO_URL}" f"/hr_attendance/attendance_user_data",
                json=payload,
                headers=self.headers,
            )
            data = response.json()
            if data.get("error"):
                message = f"Failed fetching attendance " f"state: {data['error']}"
                raise Exception(message)
            result = data["result"]
            return result

        except Exception as e:
            logger.exception(e)
            return None

    def get_attendance_stats(self):
        attendance_data = self.get_current_state()
        if not attendance_data:
            return "❌ Failed fetching " "attendance stats"
        attendance_state = attendance_data["attendance_state"]
        if attendance_state == "checked_in":
            attendance_state = Messages.ATTENDANCE_STATE_CHECKED_IN
        else:
            attendance_state = Messages.ATTENDANCE_STATE_CHECKED_OUT
        return Messages.ATTENDANCE_STATS.format(
            attendance_state,
            attendance_data.get("hours_today"),
            attendance_data.get("last_check_in"),
            attendance_data.get("last_attendance_worked_hours"),
        )

    def toggle_attendance(self):
        coordinates = self.get_coordinates()
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "latitude": (coordinates.get("lat")),
                "longitude": (coordinates.get("long")),
            },
            "id": 1,
        }
        response = self.session.post(
            f"{OdooConstants.ODOO_URL}" f"/hr_attendance/" f"systray_check_in_out",
            json=payload,
            headers=self.headers,
        )
        data = response.json()
        if data.get("error"):
            raise Exception(f"Attendance toggle failed: " f"{data['error']}")
        return data["result"]

    def check_in(self):
        try:
            attendance_data = self.get_current_state()
            current_state = attendance_data["attendance_state"]
            if current_state == "checked_in":
                logger.info("Attendance already checked in")
                return Messages.ALREADY_CHECKED_IN
            result = self.toggle_attendance()
            if result["attendance_state"] != "checked_in":
                raise Exception(Messages.CHECK_IN_FAILED)
            logger.info("Attendance check-in successful")
            message = (
                f"{Messages.CHECK_IN_SUCCESS}\n\n"
                f"{self.get_attendance_stats()}"
            )
            return message
        except Exception as e:
            logger.exception("Attendance check-in failed")
            return Messages.CHECK_IN_EXCEPTION.format(e)


    def check_out(self):
        try:
            attendance_data = self.get_current_state()
            current_state = attendance_data["attendance_state"]
            if current_state == "checked_out":
                logger.info("Attendance already checked out")
                return Messages.ALREADY_CHECKED_OUT
            result = self.toggle_attendance()
            if result["attendance_state"] != "checked_out":
                raise Exception(Messages.CHECK_OUT_FAILED)
            logger.info("Attendance check-out successful")
            message = (
                f"{Messages.CHECK_OUT_SUCCESS}\n\n"
                f"{self.get_attendance_stats()}"
            )
            return message
        except Exception as e:
            logger.exception("Attendance check-out failed")
            return Messages.CHECK_OUT_EXCEPTION.format(e)