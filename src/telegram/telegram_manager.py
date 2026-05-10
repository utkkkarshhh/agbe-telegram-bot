from src.constants.constants import Constants
from src.telegram.handlers import HelpHandler, AttendanceHandler
from src.utils import logger
from telegram import Bot, BotCommand
from telegram.ext import Application, ApplicationBuilder


class TelegramManager:

    def __init__(self):
        self.app: Application = (
            ApplicationBuilder()
            .token(Constants.TELEGRAM_BOT_TOKEN)
            .post_init(self.post_init)
            .build()
        )

        self._register_handlers()

    async def post_init(self, app: Application):

        commands = [
            BotCommand("attendance", "Attendance actions"),
            BotCommand("help", "Help menu")
        ]

        await app.bot.set_my_commands(commands)

    def _register_handlers(self):

        attendance_handler = AttendanceHandler()
        help_handler = HelpHandler()

        for handler in attendance_handler.get_handlers():
            self.app.add_handler(handler)

        self.app.add_handler(
            help_handler.get_handler()
        )

    @staticmethod
    async def send_message(chat_id: str, message: str):
        bot = Bot(token=Constants.TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=chat_id,text=message)

    def run(self):
        logger.info("Telegram Polling Started Successfully")
        self.app.run_polling()
