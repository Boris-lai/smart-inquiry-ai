import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.error import ErrorCode, ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


class APIError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: ErrorCode,
        message: str,
        details: list[ErrorDetail] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def _error_response(
    *,
    status_code: int,
    code: ErrorCode,
    message: str,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    content = ErrorResponse(
        error={
            "code": code,
            "message": message,
            "details": details,
        }
    ).model_dump(mode="json", exclude_none=True)
    return JSONResponse(status_code=status_code, content=content)


def _public_field_name(location: tuple[Any, ...]) -> str:
    public_parts = [str(part) for part in location if part not in {"body", "query", "path"}]
    return ".".join(public_parts) if public_parts else "request"


def _field_label(field_name: str) -> str:
    label = field_name.split(".")[-1].replace("_", " ")
    return label[:1].upper() + label[1:]


def _validation_message(error: dict[str, Any], field_name: str) -> str:
    error_type = str(error.get("type", ""))
    context = error.get("ctx") or {}

    if error_type == "missing":
        return f"{_field_label(field_name)} is required."

    if error_type == "extra_forbidden":
        return "Unexpected field."

    if error_type == "string_too_long":
        max_length = context.get("max_length")
        if max_length is not None:
            return f"Must be at most {max_length} characters."

    message = str(error.get("msg", "Invalid value."))
    if message.startswith("Value error, "):
        message = message.removeprefix("Value error, ")
    return message


def _validation_details(exc: RequestValidationError) -> list[ErrorDetail]:
    return [
        ErrorDetail(
            field=_public_field_name(tuple(error.get("loc", ()))),
            message=_validation_message(
                error,
                _public_field_name(tuple(error.get("loc", ()))),
            ),
        )
        for error in exc.errors()
    ]


def _http_error_code(status_code: int) -> ErrorCode:
    if status_code == HTTPStatus.BAD_REQUEST:
        return ErrorCode.BAD_REQUEST
    if status_code == HTTPStatus.NOT_FOUND:
        return ErrorCode.NOT_FOUND
    if status_code == HTTPStatus.CONFLICT:
        return ErrorCode.CONFLICT
    return ErrorCode.INTERNAL_SERVER_ERROR


def _http_error_message(status_code: int) -> str:
    if status_code == HTTPStatus.BAD_REQUEST:
        return "The request body could not be processed."
    if status_code == HTTPStatus.NOT_FOUND:
        return "Resource was not found."
    if status_code == HTTPStatus.CONFLICT:
        return "The request conflicts with the current resource state."
    return "Something went wrong. Please try again later."


async def api_error_handler(_request: Request, exc: APIError) -> JSONResponse:
    return _error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    if any(error.get("type") == "json_invalid" for error in exc.errors()):
        return _error_response(
            status_code=HTTPStatus.BAD_REQUEST,
            code=ErrorCode.BAD_REQUEST,
            message="The request body could not be processed.",
        )

    return _error_response(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        code=ErrorCode.VALIDATION_ERROR,
        message="One or more fields are invalid.",
        details=_validation_details(exc),
    )


async def http_exception_handler(
    _request: Request,
    exc: HTTPException | StarletteHTTPException,
) -> JSONResponse:
    status_code = exc.status_code
    return _error_response(
        status_code=status_code,
        code=_http_error_code(status_code),
        message=_http_error_message(status_code),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception("Unexpected API error at %s", request.url.path, exc_info=exc)
    return _error_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        code=ErrorCode.INTERNAL_SERVER_ERROR,
        message="Something went wrong. Please try again later.",
    )


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(APIError, api_error_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(StarletteHTTPException, http_exception_handler)
    application.add_exception_handler(Exception, unexpected_exception_handler)
