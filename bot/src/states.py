from collections import defaultdict
from enum import Enum

from telegram import Update


class UserStateEnum(str, Enum):
    START = 0
    REMAINS = 1
    FORECAST = 2


class UserStates:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._user_state = defaultdict(
                lambda: {"state": UserStateEnum.START, "last_uploaded_image": None}
            )
        return cls._instance

    def get_state(self, message: Update) -> int:
        return self._user_state[message.effective_chat.id]["state"]

    def update_state(self, message: Update, state: int = UserStateEnum.START):
        self._user_state[message.effective_chat.id] = {
            "state": state
        }
