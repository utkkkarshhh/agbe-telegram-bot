import json
from pathlib import Path


class UserRepository:

    FILE_PATH = Path("src/models/users.json")

    @classmethod
    def load_users(cls):
        if not cls.FILE_PATH.exists():
            return []
        with open(cls.FILE_PATH, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    @classmethod
    def save_users(cls, users):
        with open(cls.FILE_PATH, "w") as file:
            json.dump(users, file, indent=4)

    @classmethod
    def add_user(cls, user_data):
        users = cls.load_users()
        existing_user = next(
            (user for user in users if user["chat_id"] == user_data["chat_id"]), None
        )
        if existing_user:
            return
        users.append(user_data)
        cls.save_users(users)
