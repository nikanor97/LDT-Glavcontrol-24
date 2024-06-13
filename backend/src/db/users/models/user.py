from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.db.mixins import TimeStampWithIdMixin
from src.db.users.models import UsersSQLModel


class UserBase(UsersSQLModel):
    name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True, unique=True)
    permission_read_stat: bool = Field(nullable=False, default=False)
    permission_create_order: bool = Field(nullable=False, default=False)
    is_deleted: bool = Field(nullable=False, default=False)


class User(UserBase, TimeStampWithIdMixin, table=True):
    __tablename__ = "users"
