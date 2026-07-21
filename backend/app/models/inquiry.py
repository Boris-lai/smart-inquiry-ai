from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.customer import utc_now
from app.models.enums import AIGenerationStatus, AIUrgency, InquiryStatus

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.notification import Notification


class Inquiry(Base):
    __tablename__ = "inquiries"
    __table_args__ = (
        Index("idx_inquiries_customer_id", "customer_id"),
        Index("idx_inquiries_status_created_at", "status", "created_at"),
        Index("idx_inquiries_created_at", "created_at"),
        Index("idx_inquiries_ai_generation_status", "ai_generation_status"),
    )

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    customer_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    inquiry_type: Mapped[str | None] = mapped_column(VARCHAR(80), nullable=True)
    budget_range: Mapped[str | None] = mapped_column(VARCHAR(80), nullable=True)
    timeline: Mapped[str | None] = mapped_column(VARCHAR(120), nullable=True)
    message: Mapped[str] = mapped_column(TEXT, nullable=False)
    status: Mapped[InquiryStatus] = mapped_column(
        ENUM(
            InquiryStatus.NEW.value,
            InquiryStatus.IN_PROGRESS.value,
            InquiryStatus.COMPLETED.value,
            InquiryStatus.ARCHIVED.value,
            name="inquiry_status",
        ),
        nullable=False,
        default=InquiryStatus.NEW,
        server_default=text("'new'"),
    )
    ai_summary: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_customer_need: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_urgency: Mapped[AIUrgency | None] = mapped_column(
        ENUM(
            AIUrgency.LOW.value,
            AIUrgency.MEDIUM.value,
            AIUrgency.HIGH.value,
            AIUrgency.UNKNOWN.value,
            name="ai_urgency",
        ),
        nullable=True,
    )
    ai_missing_information: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_suggested_next_action: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    ai_generated_at: Mapped[datetime | None] = mapped_column(
        DATETIME(fsp=6),
        nullable=True,
    )
    ai_generation_status: Mapped[AIGenerationStatus] = mapped_column(
        ENUM(
            AIGenerationStatus.PENDING.value,
            AIGenerationStatus.SUCCEEDED.value,
            AIGenerationStatus.FAILED.value,
            name="ai_generation_status",
        ),
        nullable=False,
        default=AIGenerationStatus.PENDING,
        server_default=text("'pending'"),
    )
    ai_generation_error: Mapped[str | None] = mapped_column(TEXT, nullable=True)
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

    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="inquiries",
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="inquiry",
    )
