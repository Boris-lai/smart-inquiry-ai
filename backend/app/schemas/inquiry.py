from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    ValidationInfo,
    field_validator,
)

from app.models.enums import AIGenerationStatus, AIUrgency, InquiryStatus
from app.models.enums import PreferredContactMethod
from app.schemas.common import ApiTimestamp, PositiveId
from app.schemas.customer import CustomerCompactResponse, CustomerDetailResponse
from app.schemas.notification import NotificationResponse


OptionalShortText = Annotated[str | None, Field(default=None)]


def _normalize_optional_string(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return value


class InquiryCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_default=True)

    name: Annotated[str, Field(max_length=120)]
    email: Annotated[EmailStr, Field(max_length=255)]
    preferred_contact_method: PreferredContactMethod = PreferredContactMethod.EMAIL
    phone: Annotated[str | None, Field(default=None, max_length=50)]
    company: Annotated[str | None, Field(default=None, max_length=160)]
    inquiry_type: Annotated[str | None, Field(default=None, max_length=80)]
    budget_range: Annotated[str | None, Field(default=None, max_length=80)]
    timeline: Annotated[str | None, Field(default=None, max_length=120)]
    message: Annotated[str, Field(max_length=10000)]

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: object) -> object:
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                raise ValueError("Name is required.")
            return stripped
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator(
        "phone",
        "company",
        "inquiry_type",
        "budget_range",
        "timeline",
        mode="before",
    )
    @classmethod
    def normalize_optional_strings(cls, value: object) -> object:
        return _normalize_optional_string(value)

    @field_validator("phone")
    @classmethod
    def require_phone_for_phone_contact(
        cls,
        value: str | None,
        info: ValidationInfo,
    ) -> str | None:
        if info.data.get("preferred_contact_method") == PreferredContactMethod.PHONE:
            if value is None:
                raise ValueError(
                    "Phone is required when preferred contact method is phone."
                )
        return value

    @field_validator("message")
    @classmethod
    def require_non_blank_message(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message is required.")
        return value


class InquiryCreateResponse(BaseModel):
    inquiry_id: PositiveId
    status: InquiryStatus
    ai_generation_status: AIGenerationStatus
    message: str


class InquiryListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: Annotated[int, Field(default=1, ge=1)]
    page_size: Annotated[int, Field(default=20, ge=1, le=100)]
    status: InquiryStatus | None = None
    ai_generation_status: AIGenerationStatus | None = None
    sort: Literal["created_at", "-created_at"] = "-created_at"


class InquiryListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveId
    status: InquiryStatus
    inquiry_type: str | None = None
    customer: CustomerCompactResponse
    ai_generation_status: AIGenerationStatus
    ai_summary_preview: str | None = None
    created_at: ApiTimestamp
    updated_at: ApiTimestamp


class InquiryListMeta(BaseModel):
    page: Annotated[int, Field(ge=1)]
    page_size: Annotated[int, Field(ge=1, le=100)]
    total: Annotated[int, Field(ge=0)]
    has_next: bool
    sort: Literal["created_at", "-created_at"]


class InquiryListResponse(BaseModel):
    items: list[InquiryListItemResponse]
    meta: InquiryListMeta


class InquiryAIResponse(BaseModel):
    generation_status: AIGenerationStatus
    summary: str | None = None
    customer_need: str | None = None
    urgency: AIUrgency | None = None
    missing_information: str | None = None
    suggested_next_action: str | None = None
    generated_at: ApiTimestamp | None = None


class InquiryDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveId
    status: InquiryStatus
    inquiry_type: str | None = None
    budget_range: str | None = None
    timeline: str | None = None
    message: str
    customer: CustomerDetailResponse
    ai: InquiryAIResponse
    notifications: list[NotificationResponse]
    created_at: ApiTimestamp
    updated_at: ApiTimestamp


class InquiryStatusUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: InquiryStatus


class InquiryStatusUpdateResponse(BaseModel):
    id: PositiveId
    status: InquiryStatus
    updated_at: ApiTimestamp

