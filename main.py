from src.telegram import TelegramManager

from src.constants import Constants
from src.utils import logger

def main():
    BOT_NAME = Constants.BOT_NAME
    try:
        logger.info(f"{BOT_NAME} is starting...")
        telegram_manager = TelegramManager()
        telegram_manager.run()
        logger.info(f"{BOT_NAME} has been stopped successfully")
    except KeyboardInterrupt as ke:
        logger.warning(f"{BOT_NAME} has been stopped")
    except Exception as error:
        logger.error(f"{BOT_NAME} stopped unexpectedly : {error}")

if __name__ == "__main__":
    main()
