from typing import Dict

import requests

from src.constants import OdooConstants
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
            }
        }
        response = self.session.post(
            f"{OdooConstants.ODOO_URL}/web/session/authenticate",
            json=payload,
            headers=self.headers
        )
        data = response.json()
        if data.get("error"):
            raise Exception(f"Authentication failed: {data['error']}")
        logger.info("Odoo Authentication Successfull")

    def get_coordinates(self) -> Dict:
        if DateTimeUtils.get_current_day_name() in OdooConstants.WORK_FROM_HOME_DAYS:
            return OdooConstants.HOME_COORDINATES
        else: return OdooConstants.AGBE_COORDINATES

    def get_current_state(self):
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {},
                "id": 1
            }
            response = self.session.post(
                f"{OdooConstants.ODOO_URL}/hr_attendance/attendance_user_data",
                json=payload,
                headers=self.headers
            )
            data = response.json()
            if data.get("error"):
                message = f"Failed fetching attendance state: {data['error']}"
                raise Exception(message)
            result = data["result"]
            current_state = result["attendance_state"]
            logger.debug(f"Current State is {current_state}")
            return current_state
        except Exception as e:
            logger.exception(e)
            return e

    def toggle_attendance(self):
        coordinates = self.get_coordinates()
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "latitude": coordinates.get('lat'),
                "longitude": coordinates.get('long')
            },
            "id": 1
        }
        response = self.session.post(
            f"{OdooConstants.ODOO_URL}/hr_attendance/systray_check_in_out",
            json=payload,
            headers=self.headers)
        data = response.json()
        if data.get("error"):
            raise Exception(f"Attendance toggle failed: {data['error']}")
        return data["result"]
    
    def check_in(self):
        try:
            current_state = self.get_current_state()
            if current_state == "checked_in":
                message = "Already checked in"
                logger.debug(message)
                return message
            result = self.toggle_attendance()
            if result["attendance_state"] != "checked_in":
                message = "Check-in failed unexpectedly"
                raise Exception(message)
            message = "Check-in successful"
            logger.debug(message)
            return message
        except Exception as e:
            logger.exception(e)
            return e

    def check_out(self):
        try:
            current_state = self.get_current_state()
            if current_state == "checked_out":
                message = "Already checked out"
                logger.debug(message)
                return message
            result = self.toggle_attendance()
            if result["attendance_state"] != "checked_out":
                message = "Check-in failed unexpectedly"
                raise Exception(message)
            message = "Check-out successful"
            logger.debug(message)
            return message
        except Exception as e:
            logger.exception(e)
            return e
