from pydantic import BaseModel, ConfigDict

from app.models.enums import NotificationDeliveryStatus
from app.schemas.common import ApiTimestamp, PositiveId


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveId
    notification_type: str
    channel: str
    recipient: str
    delivery_status: NotificationDeliveryStatus
    provider_name: str | None = None
    provider_message_id: str | None = None
    error_message: str | None = None
    attempted_at: ApiTimestamp | None = None
    sent_at: ApiTimestamp | None = None
    created_at: ApiTimestamp
    updated_at: ApiTimestamp

