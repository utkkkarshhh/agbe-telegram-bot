from src.managers.odoo_manager import OdooManager
from src.telegram.keyboards.attendance_keyboard import AttendanceKeyboard
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters


class AttendanceHandler:

    def __init__(self):
        self.odoo_manager = OdooManager()
        self.odoo_manager.authenticate()

    def get_handlers(self):
        return [
            CommandHandler("attendance",self.attendance_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND,self.handle_message)
        ]

    async def attendance_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        reply_markup = (AttendanceKeyboard.get_keyboard())
        await update.message.reply_text(
            text="Choose attendance action:",
            reply_markup=reply_markup
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):
        message = update.message.text
        try:
            if message == "Check In":
                response = self.odoo_manager.check_in()

            elif message == "Check Out":
                response= self.odoo_manager.check_out()

            elif message == "Current Status":
                current_state = self.odoo_manager.get_current_state()
                response = f"Current Attendance Status: '{current_state}'"
    
            else:
                return

            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
