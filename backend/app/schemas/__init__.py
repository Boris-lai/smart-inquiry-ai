from app.schemas.customer import CustomerCompactResponse, CustomerDetailResponse
from app.schemas.error import ErrorBody, ErrorCode, ErrorDetail, ErrorResponse
from app.schemas.inquiry import (
    InquiryAIResponse,
    InquiryCreateRequest,
    InquiryCreateResponse,
    InquiryDetailResponse,
    InquiryListItemResponse,
    InquiryListMeta,
    InquiryListQuery,
    InquiryListResponse,
    InquiryStatusUpdateRequest,
    InquiryStatusUpdateResponse,
)
from app.schemas.notification import NotificationResponse

__all__ = [
    "CustomerCompactResponse",
    "CustomerDetailResponse",
    "ErrorBody",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "InquiryAIResponse",
    "InquiryCreateRequest",
    "InquiryCreateResponse",
    "InquiryDetailResponse",
    "InquiryListItemResponse",
    "InquiryListMeta",
    "InquiryListQuery",
    "InquiryListResponse",
    "InquiryStatusUpdateRequest",
    "InquiryStatusUpdateResponse",
    "NotificationResponse",
]
