import uuid
from collections import defaultdict
from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlmodel import col
from src.db.base_manager import BaseDbManager
from src.db.exceptions import ResourceAlreadyExists


class ProjectsDbManager(BaseDbManager):
    pass