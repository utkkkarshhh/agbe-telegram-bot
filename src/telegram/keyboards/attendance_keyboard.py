from telegram import ReplyKeyboardMarkup


class AttendanceKeyboard:
    CHECK_IN = "Check In"
    CHECK_OUT = "Check Out"
    CURRENT_STATUS = "Current Stats"

    @staticmethod
    def get_keyboard():

        keyboard = [
            [AttendanceKeyboard.CHECK_IN, AttendanceKeyboard.CHECK_OUT],
            [AttendanceKeyboard.CURRENT_STATUS],
        ]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
