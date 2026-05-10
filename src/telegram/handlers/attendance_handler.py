from src.managers import OdooManager
from src.telegram.keyboards import AttendanceKeyboard
from src.telegram.telegram_user_manager import TelegramUserManager
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters


class AttendanceHandler:
    def __init__(self):
        self.odoo_manager = OdooManager()
        self.odoo_manager.authenticate()

    def get_handlers(self):
        return [
            CommandHandler("attendance", self.attendance_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message),
        ]

    async def attendance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.register_user(update)
        reply_markup = AttendanceKeyboard.get_keyboard()
        await update.message.reply_text(
            text="Choose attendance action:", reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.register_user(update)
        message = update.message.text

        try:
            if message == AttendanceKeyboard.CHECK_IN:
                response = self.odoo_manager.check_in()
            elif message == AttendanceKeyboard.CHECK_OUT:
                response = self.odoo_manager.check_out()
            elif message == AttendanceKeyboard.CURRENT_STATUS:
                response = self.odoo_manager.get_attendance_stats()
            else:
                return
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

    def register_user(self, update: Update):
        TelegramUserManager.register_user(
            chat_id=(update.effective_chat.id),
            username=(update.effective_user.username),
            first_name=(update.effective_user.first_name),
        )
