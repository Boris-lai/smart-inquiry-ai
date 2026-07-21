from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.enums import AIGenerationStatus, InquiryStatus, PreferredContactMethod
from app.schemas.inquiry import (
    InquiryCreateRequest,
    InquiryCreateResponse,
    InquiryListItemResponse,
    InquiryStatusUpdateRequest,
    InquiryStatusUpdateResponse,
)


def test_inquiry_create_request_normalizes_public_input() -> None:
    request = InquiryCreateRequest.model_validate(
        {
            "name": "  Alex Chen  ",
            "email": " Alex@Example.COM ",
            "phone": "   ",
            "company": " Northstar Studio ",
            "inquiry_type": " website redesign ",
            "budget_range": "",
            "timeline": " within 2 months ",
            "message": "  We need help improving inquiry conversion.  ",
        }
    )

    assert request.name == "Alex Chen"
    assert str(request.email) == "alex@example.com"
    assert request.preferred_contact_method == PreferredContactMethod.EMAIL
    assert request.phone is None
    assert request.company == "Northstar Studio"
    assert request.inquiry_type == "website redesign"
    assert request.budget_range is None
    assert request.timeline == "within 2 months"
    assert request.message == "  We need help improving inquiry conversion.  "


def test_inquiry_create_request_rejects_internal_fields() -> None:
    with pytest.raises(ValidationError) as exc_info:
        InquiryCreateRequest.model_validate(
            {
                "name": "Alex Chen",
                "email": "alex@example.com",
                "message": "Need help.",
                "status": "completed",
            }
        )

    error = exc_info.value.errors()[0]
    assert error["loc"] == ("status",)
    assert error["type"] == "extra_forbidden"


def test_inquiry_create_request_requires_phone_for_phone_contact() -> None:
    with pytest.raises(ValidationError) as exc_info:
        InquiryCreateRequest.model_validate(
            {
                "name": "Alex Chen",
                "email": "alex@example.com",
                "preferred_contact_method": "phone",
                "phone": " ",
                "message": "Need help.",
            }
        )

    error = exc_info.value.errors()[0]
    assert error["loc"] == ("phone",)
    assert "Phone is required" in error["msg"]


def test_inquiry_create_request_rejects_blank_required_fields() -> None:
    with pytest.raises(ValidationError) as exc_info:
        InquiryCreateRequest.model_validate(
            {
                "name": " ",
                "email": "alex@example.com",
                "message": " ",
            }
        )

    errors = {error["loc"][0]: error["msg"] for error in exc_info.value.errors()}
    assert "Name is required." in errors["name"]
    assert "Message is required." in errors["message"]


def test_success_response_schema_matches_public_contract() -> None:
    response = InquiryCreateResponse(
        inquiry_id=101,
        status=InquiryStatus.NEW,
        ai_generation_status=AIGenerationStatus.PENDING,
        message="Your inquiry was received successfully.",
    )

    assert response.model_dump(mode="json") == {
        "inquiry_id": 101,
        "status": "new",
        "ai_generation_status": "pending",
        "message": "Your inquiry was received successfully.",
    }


def test_dashboard_response_timestamps_serialize_as_utc_iso8601() -> None:
    response = InquiryStatusUpdateResponse(
        id=101,
        status=InquiryStatus.IN_PROGRESS,
        updated_at=datetime(2026, 7, 20, 9, 15, tzinfo=UTC),
    )

    assert response.model_dump(mode="json") == {
        "id": 101,
        "status": "in_progress",
        "updated_at": "2026-07-20T09:15:00Z",
    }


def test_list_item_response_uses_snake_case_contract_fields() -> None:
    response = InquiryListItemResponse(
        id=101,
        status=InquiryStatus.NEW,
        inquiry_type="website redesign",
        customer={
            "name": "Alex Chen",
            "email": "alex@example.com",
            "company": "Northstar Studio",
        },
        ai_generation_status=AIGenerationStatus.PENDING,
        ai_summary_preview=None,
        created_at=datetime(2026, 7, 20, 8, 30),
        updated_at=datetime(2026, 7, 20, 8, 30),
    )

    assert response.model_dump(mode="json") == {
        "id": 101,
        "status": "new",
        "inquiry_type": "website redesign",
        "customer": {
            "name": "Alex Chen",
            "email": "alex@example.com",
            "company": "Northstar Studio",
        },
        "ai_generation_status": "pending",
        "ai_summary_preview": None,
        "created_at": "2026-07-20T08:30:00Z",
        "updated_at": "2026-07-20T08:30:00Z",
    }


def test_status_update_request_accepts_only_approved_status_values() -> None:
    request = InquiryStatusUpdateRequest.model_validate({"status": "archived"})

    assert request.status == InquiryStatus.ARCHIVED

    with pytest.raises(ValidationError):
        InquiryStatusUpdateRequest.model_validate({"status": "deleted"})

