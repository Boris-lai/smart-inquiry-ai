import logging
from dataclasses import dataclass
from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import APIError
from app.models.customer import Customer
from app.models.enums import AIGenerationStatus, InquiryStatus
from app.models.inquiry import Inquiry
from app.repositories import customer as customer_repository
from app.repositories import inquiry as inquiry_repository
from app.schemas.error import ErrorCode
from app.schemas.inquiry import InquiryCreateRequest

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InquirySubmissionResult:
    inquiry_id: int
    status: InquiryStatus
    ai_generation_status: AIGenerationStatus
    message: str


def submit_public_inquiry(
    db: Session,
    request: InquiryCreateRequest,
) -> InquirySubmissionResult:
    try:
        customer = _get_or_prepare_customer(db, request)
        inquiry = Inquiry(
            customer_id=customer.id,
            inquiry_type=request.inquiry_type,
            budget_range=request.budget_range,
            timeline=request.timeline,
            message=request.message,
            status=InquiryStatus.NEW,
            ai_generation_status=AIGenerationStatus.PENDING,
        )
        inquiry_repository.add_inquiry(db, inquiry)
        db.flush()

        inquiry_id = inquiry.id
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Inquiry submission database operation failed.")
        raise APIError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message="Something went wrong. Please try again later.",
        ) from exc

    # AI generation and notification dispatch are intentionally added after Day 7.
    return InquirySubmissionResult(
        inquiry_id=inquiry_id,
        status=InquiryStatus.NEW,
        ai_generation_status=AIGenerationStatus.PENDING,
        message="Your inquiry was received successfully.",
    )


def _get_or_prepare_customer(
    db: Session,
    request: InquiryCreateRequest,
) -> Customer:
    normalized_email = str(request.email)
    customer = customer_repository.get_customer_by_email(db, normalized_email)

    if customer is None:
        customer = Customer(
            name=request.name,
            email=normalized_email,
            phone=request.phone,
            company=request.company,
            preferred_contact_method=request.preferred_contact_method,
        )
        customer_repository.add_customer(db, customer)
        db.flush()
        return customer

    customer.name = request.name
    if request.phone is not None:
        customer.phone = request.phone
    if request.company is not None:
        customer.company = request.company
    if "preferred_contact_method" in request.model_fields_set:
        customer.preferred_contact_method = request.preferred_contact_method

    return customer

