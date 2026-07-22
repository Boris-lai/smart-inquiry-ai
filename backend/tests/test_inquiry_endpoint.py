from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from app.models.enums import AIGenerationStatus, InquiryStatus
from app.schemas.inquiry import InquiryCreateRequest
from app.services.inquiry import InquirySubmissionResult


class FakeDb:
    pass


def test_valid_submission_returns_201_and_approved_response(
    monkeypatch,
) -> None:
    fake_db = FakeDb()
    captured: dict[str, object] = {}

    def override_db():
        yield fake_db

    def fake_submit(db, request: InquiryCreateRequest) -> InquirySubmissionResult:
        captured["db"] = db
        captured["request"] = request
        return InquirySubmissionResult(
            inquiry_id=101,
            status=InquiryStatus.NEW,
            ai_generation_status=AIGenerationStatus.PENDING,
            message="Your inquiry was received successfully.",
        )

    from app.api.v1.endpoints import inquiries

    monkeypatch.setattr(inquiries, "submit_public_inquiry", fake_submit)
    app.dependency_overrides[get_db] = override_db
    try:
        client = TestClient(app)
        response = client.post(
            "/api/v1/inquiries",
            json={
                "name": " Alex Chen ",
                "email": " Alex@Example.COM ",
                "phone": " ",
                "company": " Northstar Studio ",
                "inquiry_type": " website redesign ",
                "budget_range": "",
                "timeline": " within 2 months ",
                "message": "Need help improving inquiry conversion.",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json() == {
        "inquiry_id": 101,
        "status": "new",
        "ai_generation_status": "pending",
        "message": "Your inquiry was received successfully.",
    }
    assert captured["db"] is fake_db
    request = captured["request"]
    assert isinstance(request, InquiryCreateRequest)
    assert request.name == "Alex Chen"
    assert str(request.email) == "alex@example.com"
    assert request.phone is None
    assert request.company == "Northstar Studio"
    assert request.inquiry_type == "website redesign"
    assert request.budget_range is None
    assert request.timeline == "within 2 months"


def test_invalid_email_returns_standard_422_envelope() -> None:
    response = TestClient(app).post(
        "/api/v1/inquiries",
        json={
            "name": "Alex Chen",
            "email": "not-an-email",
            "message": "Need help.",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["details"][0]["field"] == "email"


def test_blank_name_returns_standard_422_envelope() -> None:
    response = TestClient(app).post(
        "/api/v1/inquiries",
        json={
            "name": " ",
            "email": "alex@example.com",
            "message": "Need help.",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["details"] == [
        {"field": "name", "message": "Name is required."}
    ]


def test_blank_message_returns_standard_422_envelope() -> None:
    response = TestClient(app).post(
        "/api/v1/inquiries",
        json={
            "name": "Alex Chen",
            "email": "alex@example.com",
            "message": " ",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["details"] == [
        {"field": "message", "message": "Message is required."}
    ]


def test_phone_preference_without_phone_returns_phone_detail() -> None:
    response = TestClient(app).post(
        "/api/v1/inquiries",
        json={
            "name": "Alex Chen",
            "email": "alex@example.com",
            "preferred_contact_method": "phone",
            "message": "Need help.",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["details"] == [
        {
            "field": "phone",
            "message": "Phone is required when preferred contact method is phone.",
        }
    ]


def test_internal_request_fields_are_rejected() -> None:
    response = TestClient(app).post(
        "/api/v1/inquiries",
        json={
            "name": "Alex Chen",
            "email": "alex@example.com",
            "message": "Need help.",
            "customer_id": 1,
            "status": "completed",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"] == {
        "code": "validation_error",
        "message": "One or more fields are invalid.",
        "details": [
            {"field": "customer_id", "message": "Unexpected field."},
            {"field": "status", "message": "Unexpected field."},
        ],
    }


def test_service_failure_returns_safe_500_envelope(monkeypatch) -> None:
    def override_db():
        yield FakeDb()

    def fail_submit(_db, _request: InquiryCreateRequest) -> InquirySubmissionResult:
        raise RuntimeError("database driver detail should stay private")

    from app.api.v1.endpoints import inquiries

    monkeypatch.setattr(inquiries, "submit_public_inquiry", fail_submit)
    app.dependency_overrides[get_db] = override_db
    try:
        response = TestClient(app, raise_server_exceptions=False).post(
            "/api/v1/inquiries",
            json={
                "name": "Alex Chen",
                "email": "alex@example.com",
                "message": "Need help.",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "Something went wrong. Please try again later.",
        }
    }
    assert "database driver detail" not in response.text


def test_openapi_documents_public_inquiry_submission() -> None:
    schema = TestClient(app).get("/openapi.json").json()
    operation = schema["paths"]["/api/v1/inquiries"]["post"]

    assert "201" in operation["responses"]
    request_ref = operation["requestBody"]["content"]["application/json"]["schema"][
        "$ref"
    ]
    response_ref = operation["responses"]["201"]["content"]["application/json"][
        "schema"
    ]["$ref"]
    assert request_ref.endswith("/InquiryCreateRequest")
    assert response_ref.endswith("/InquiryCreateResponse")

