from fastapi import Body, FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import APIError, register_exception_handlers
from app.schemas.error import ErrorCode, ErrorDetail
from app.schemas.inquiry import InquiryCreateRequest


def _test_client() -> TestClient:
    application = FastAPI()
    register_exception_handlers(application)

    @application.post("/validation")
    def validation_target(payload: InquiryCreateRequest) -> dict[str, object]:
        return payload.model_dump(mode="json")

    @application.post("/json")
    def json_target(payload: dict[str, object] = Body(...)) -> dict[str, object]:
        return payload

    @application.get("/api-error")
    def api_error_target() -> None:
        raise APIError(
            status_code=404,
            code=ErrorCode.NOT_FOUND,
            message="Inquiry was not found.",
        )

    @application.get("/unsupported-transition")
    def unsupported_transition_target() -> None:
        raise APIError(
            status_code=409,
            code=ErrorCode.UNSUPPORTED_STATUS_TRANSITION,
            message="The requested status transition is not allowed.",
            details=[
                ErrorDetail(
                    field="status",
                    message="The requested transition is not allowed.",
                )
            ],
        )

    @application.get("/unexpected")
    def unexpected_target() -> None:
        raise RuntimeError("database password leaked-looking detail")

    return TestClient(application, raise_server_exceptions=False)


def test_validation_errors_use_standard_envelope_without_location_prefixes() -> None:
    client = _test_client()

    response = client.post(
        "/validation",
        json={
            "name": "Alex Chen",
            "email": "alex@example.com",
            "preferred_contact_method": "phone",
            "phone": " ",
            "message": "Need help.",
            "status": "completed",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "validation_error",
            "message": "One or more fields are invalid.",
            "details": [
                {
                    "field": "phone",
                    "message": "Phone is required when preferred contact method is phone.",
                },
                {"field": "status", "message": "Unexpected field."},
            ],
        }
    }


def test_malformed_json_uses_bad_request_envelope() -> None:
    client = _test_client()

    response = client.post(
        "/json",
        content='{"name": ',
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "bad_request",
            "message": "The request body could not be processed.",
        }
    }


def test_api_error_uses_standard_envelope() -> None:
    client = _test_client()

    response = client.get("/api-error")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Inquiry was not found.",
        }
    }


def test_conflict_error_can_use_approved_unsupported_transition_code() -> None:
    client = _test_client()

    response = client.get("/unsupported-transition")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "unsupported_status_transition",
            "message": "The requested status transition is not allowed.",
            "details": [
                {
                    "field": "status",
                    "message": "The requested transition is not allowed.",
                }
            ],
        }
    }


def test_default_404_uses_standard_envelope() -> None:
    client = _test_client()

    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Resource was not found.",
        }
    }


def test_unexpected_exceptions_return_safe_internal_error() -> None:
    client = _test_client()

    response = client.get("/unexpected")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "Something went wrong. Please try again later.",
        }
    }
    assert "RuntimeError" not in response.text
    assert "database password" not in response.text

