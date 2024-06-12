from datetime import datetime
from typing import Protocol, TypeVar, Generic, Optional, Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel


class METHOD:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class RouterProtocol(Protocol):
    router: APIRouter


def _http_error(error: str, msg: str) -> dict:
    return {
        "code": error,
        "message": msg,
    }


Model_T = TypeVar("Model_T", bound=BaseModel | list)


class Pagination(BaseModel):
    offset: int
    limit: int
    count: int


class UnifiedResponse(GenericModel, Generic[Model_T]):
    # data: Optional[Model_T | list[Model_T]] = None
    data: Optional[Model_T] = None
    error: Optional[str] = None  # list here cause error is always exception.args
    error_metadata: Optional[Any] = None
    status_code: int = 200

    @validator("data")
    def data_is_empty_list(cls, v):
        """
        Without this validator if data is an empty list, UnifiedResponse validation will fail.

        Somehow if data is an empty list, it is considered by pydantic as BaseModel()
        """
        return [] if v == BaseModel() else v


class DataWithPagination(GenericModel, Generic[Model_T]):
    items: Model_T
    pagination: Pagination


class UnifiedResponsePaginated(GenericModel, Generic[Model_T]):
    data: Optional[DataWithPagination[Model_T]] = None
    error: Optional[str] = None  # list here cause error is always exception.args
    error_metadata: Optional[Any] = None
    status_code: int = 200

    @validator("data")
    def data_is_empty_list(cls, v):
        """
        Without this validator if data is an empty list, UnifiedResponse validation will fail.

        Somehow if data is an empty list, it is considered by pydantic as BaseModel()
        """
        if v is None:
            return None
        elif v.items == BaseModel():
            v.items = []
        return v


class ModelWithLabelAndValue(GenericModel, Generic[Model_T]):
    label: str
    value: Model_T


def exc_to_str(exception: Exception) -> str:
    return "\n".join([arg for arg in exception.args])


class IdTimestampServerModelMixin(BaseModel):
    """Mixin for models that we "extend" with Relationships in API responses."""

    id: UUID
    created_at: datetime
    updated_at: datetime
