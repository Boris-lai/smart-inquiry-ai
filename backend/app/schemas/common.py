from datetime import UTC, datetime
from typing import Annotated

from pydantic import ConfigDict, Field, PlainSerializer


def serialize_utc_datetime(value: datetime) -> str:
    if value.tzinfo is not None:
        value = value.astimezone(UTC).replace(tzinfo=None)

    timespec = "microseconds" if value.microsecond else "seconds"
    return f"{value.isoformat(timespec=timespec)}Z"


ApiTimestamp = Annotated[
    datetime,
    PlainSerializer(serialize_utc_datetime, return_type=str, when_used="json"),
]
PositiveId = Annotated[int, Field(gt=0)]
ORM_MODEL_CONFIG = ConfigDict(from_attributes=True)

