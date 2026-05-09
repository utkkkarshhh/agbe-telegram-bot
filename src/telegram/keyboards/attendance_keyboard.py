from telegram import ReplyKeyboardMarkup


class AttendanceKeyboard:

    @staticmethod
    def get_keyboard():

        keyboard = [
            ["Check In", "Check Out"],
            ["Current Status"]
        ]

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
