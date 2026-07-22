from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.inquiry import InquiryCreateRequest, InquiryCreateResponse
from app.services.inquiry import submit_public_inquiry

router = APIRouter()


@router.post(
    "/inquiries",
    response_model=InquiryCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_inquiry(
    request: InquiryCreateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> InquiryCreateResponse:
    result = submit_public_inquiry(db, request)
    return InquiryCreateResponse(
        inquiry_id=result.inquiry_id,
        status=result.status,
        ai_generation_status=result.ai_generation_status,
        message=result.message,
    )

