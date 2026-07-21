from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import PreferredContactMethod
from app.schemas.common import PositiveId


class CustomerCompactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    company: str | None = None


class CustomerDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveId
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    preferred_contact_method: PreferredContactMethod

