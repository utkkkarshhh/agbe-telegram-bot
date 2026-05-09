from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)


class HelpHandler:

    def get_handler(self):
        return CommandHandler("help",self.help_command)

    async def help_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        help_text = """
Available commands:

/attendance
/help
"""
        await update.message.reply_text(help_text)
