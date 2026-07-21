from enum import Enum

from pydantic import BaseModel


class ErrorCode(str, Enum):
    BAD_REQUEST = "bad_request"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNSUPPORTED_STATUS_TRANSITION = "unsupported_status_transition"
    INTERNAL_SERVER_ERROR = "internal_server_error"


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorBody(BaseModel):
    code: ErrorCode
    message: str
    details: list[ErrorDetail] | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody

