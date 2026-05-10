from src.repositories import UserRepository
from src.utils import logger


class TelegramUserManager:
    @staticmethod
    def register_user(
        chat_id: int,
        username: str = None,
        first_name: str = None,
    ):
        users = UserRepository.load_users()
        existing_user = next(
            (
                user
                for user in users
                if user["chat_id"] == chat_id
            ),
            None,
        )
        if existing_user:
            return
        user_data = {
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name,
        }
        UserRepository.add_user(user_data)
        logger.info(f"Telegram user registered: {chat_id}")

    @staticmethod
    def get_all_users():
        return UserRepository.load_users()
