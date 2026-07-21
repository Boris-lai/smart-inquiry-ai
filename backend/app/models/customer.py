from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import PreferredContactMethod

if TYPE_CHECKING:
    from app.models.inquiry import Inquiry


def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (UniqueConstraint("email", name="uq_customers_email"),)

    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(VARCHAR(120), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True)
    company: Mapped[str | None] = mapped_column(VARCHAR(160), nullable=True)
    preferred_contact_method: Mapped[PreferredContactMethod] = mapped_column(
        ENUM(
            PreferredContactMethod.EMAIL.value,
            PreferredContactMethod.PHONE.value,
            name="preferred_contact_method",
        ),
        nullable=False,
        default=PreferredContactMethod.EMAIL,
        server_default=text("'email'"),
    )
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

    inquiries: Mapped[list["Inquiry"]] = relationship(
        "Inquiry",
        back_populates="customer",
    )
