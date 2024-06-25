from typing import TYPE_CHECKING

from pydantic import validator
from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.users.models import UsersSQLModel


class UserBase(UsersSQLModel):
    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True, unique=True)
    permission_read_stat: bool = Field(nullable=False, default=False)
    permission_create_order: bool = Field(nullable=False, default=False)
    is_deleted: bool = Field(nullable=False, default=False)
    role: str = Field(nullable=False, default="user")  # admin | user
    telegram_username: str | None = Field(nullable=True, default=None)

    @validator('telegram_username', pre=True, always=True)
    def normalize_telegram_username(cls, v):
        if v:
            v = v.lower()
            if v.startswith('@'):
                v = v[1:]
        return v


class User(UserBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "users"
