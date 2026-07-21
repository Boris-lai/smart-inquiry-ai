from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.customer import utc_now
from app.models.enums import NotificationDeliveryStatus

if TYPE_CHECKING:
    from app.models.inquiry import Inquiry


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        UniqueConstraint(
            "provider_name",
            "provider_message_id",
            name="uq_notifications_provider_message",
        ),
        Index("idx_notifications_inquiry_id", "inquiry_id"),
        Index("idx_notifications_delivery_status", "delivery_status"),
        Index("idx_notifications_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    inquiry_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("inquiries.id", ondelete="RESTRICT"),
        nullable=False,
    )
    notification_type: Mapped[str] = mapped_column(
        VARCHAR(80),
        nullable=False,
        default="new_inquiry",
        server_default=text("'new_inquiry'"),
    )
    channel: Mapped[str] = mapped_column(
        VARCHAR(40),
        nullable=False,
        default="email",
        server_default=text("'email'"),
    )
    recipient: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    delivery_status: Mapped[NotificationDeliveryStatus] = mapped_column(
        ENUM(
            NotificationDeliveryStatus.PENDING.value,
            NotificationDeliveryStatus.SENT.value,
            NotificationDeliveryStatus.FAILED.value,
            name="notification_delivery_status",
        ),
        nullable=False,
        default=NotificationDeliveryStatus.PENDING,
        server_default=text("'pending'"),
    )
    provider_name: Mapped[str | None] = mapped_column(VARCHAR(80), nullable=True)
    provider_message_id: Mapped[str | None] = mapped_column(
        VARCHAR(255),
        nullable=True,
    )
    error_message: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    attempted_at: Mapped[datetime | None] = mapped_column(
        DATETIME(fsp=6),
        nullable=True,
    )
    sent_at: Mapped[datetime | None] = mapped_column(DATETIME(fsp=6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6),
        nullable=False,
        default=utc_now,
        server_default=text("CURRENT_TIMESTAMP(6)"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=text("CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"),
    )

    inquiry: Mapped["Inquiry"] = relationship(
        "Inquiry",
        back_populates="notifications",
    )
