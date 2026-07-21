from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM

from app.db.base import Base
from app.models import (
    AIGenerationStatus,
    AIUrgency,
    Customer,
    Inquiry,
    InquiryStatus,
    Notification,
    NotificationDeliveryStatus,
    PreferredContactMethod,
)


def _index_names(table_name: str) -> set[str]:
    return {index.name for index in Base.metadata.tables[table_name].indexes}


def _unique_constraint_names(table_name: str) -> set[str]:
    return {
        constraint.name
        for constraint in Base.metadata.tables[table_name].constraints
        if isinstance(constraint, UniqueConstraint)
    }


def test_metadata_contains_exact_active_mvp_tables() -> None:
    assert set(Base.metadata.tables) == {"customers", "inquiries", "notifications"}
    assert "attachments" not in Base.metadata.tables


def test_enum_values_match_approved_contracts() -> None:
    assert [value.value for value in PreferredContactMethod] == ["email", "phone"]
    assert [value.value for value in InquiryStatus] == [
        "new",
        "in_progress",
        "completed",
        "archived",
    ]
    assert [value.value for value in AIUrgency] == [
        "low",
        "medium",
        "high",
        "unknown",
    ]
    assert [value.value for value in AIGenerationStatus] == [
        "pending",
        "succeeded",
        "failed",
    ]
    assert [value.value for value in NotificationDeliveryStatus] == [
        "pending",
        "sent",
        "failed",
    ]


def test_customer_schema_metadata_matches_approved_contract() -> None:
    table = Customer.__table__

    assert isinstance(table.c.id.type, BIGINT)
    assert table.c.id.type.unsigned is True
    assert table.c.name.type.length == 120
    assert table.c.email.type.length == 255
    assert table.c.phone.type.length == 50
    assert table.c.company.type.length == 160
    assert table.c.name.nullable is False
    assert table.c.email.nullable is False
    assert table.c.phone.nullable is True
    assert table.c.company.nullable is True
    assert isinstance(table.c.preferred_contact_method.type, ENUM)
    assert table.c.preferred_contact_method.type.enums == ["email", "phone"]
    assert str(table.c.preferred_contact_method.server_default.arg) == "'email'"
    assert isinstance(table.c.created_at.type, DATETIME)
    assert isinstance(table.c.updated_at.type, DATETIME)
    assert table.c.created_at.type.fsp == 6
    assert table.c.updated_at.type.fsp == 6
    assert "uq_customers_email" in _unique_constraint_names("customers")


def test_inquiry_schema_metadata_matches_approved_contract() -> None:
    table = Inquiry.__table__

    assert isinstance(table.c.id.type, BIGINT)
    assert table.c.id.type.unsigned is True
    assert isinstance(table.c.customer_id.type, BIGINT)
    assert table.c.customer_id.type.unsigned is True
    assert table.c.inquiry_type.type.length == 80
    assert table.c.budget_range.type.length == 80
    assert table.c.timeline.type.length == 120
    assert table.c.message.nullable is False
    assert table.c.status.type.enums == [
        "new",
        "in_progress",
        "completed",
        "archived",
    ]
    assert str(table.c.status.server_default.arg) == "'new'"
    assert table.c.ai_urgency.type.enums == ["low", "medium", "high", "unknown"]
    assert table.c.ai_generation_status.type.enums == [
        "pending",
        "succeeded",
        "failed",
    ]
    assert str(table.c.ai_generation_status.server_default.arg) == "'pending'"
    assert table.c.ai_summary.nullable is True
    assert table.c.ai_customer_need.nullable is True
    assert table.c.ai_missing_information.nullable is True
    assert table.c.ai_suggested_next_action.nullable is True
    assert table.c.ai_generated_at.nullable is True
    assert table.c.ai_generation_error.nullable is True
    assert table.c.created_at.type.fsp == 6
    assert table.c.updated_at.type.fsp == 6
    assert _index_names("inquiries") == {
        "idx_inquiries_customer_id",
        "idx_inquiries_status_created_at",
        "idx_inquiries_created_at",
        "idx_inquiries_ai_generation_status",
    }


def test_notification_schema_metadata_matches_approved_contract() -> None:
    table = Notification.__table__

    assert isinstance(table.c.id.type, BIGINT)
    assert table.c.id.type.unsigned is True
    assert isinstance(table.c.inquiry_id.type, BIGINT)
    assert table.c.inquiry_id.type.unsigned is True
    assert table.c.notification_type.type.length == 80
    assert table.c.channel.type.length == 40
    assert table.c.recipient.type.length == 255
    assert table.c.provider_name.type.length == 80
    assert table.c.provider_message_id.type.length == 255
    assert str(table.c.notification_type.server_default.arg) == "'new_inquiry'"
    assert str(table.c.channel.server_default.arg) == "'email'"
    assert table.c.delivery_status.type.enums == ["pending", "sent", "failed"]
    assert str(table.c.delivery_status.server_default.arg) == "'pending'"
    assert table.c.provider_name.nullable is True
    assert table.c.provider_message_id.nullable is True
    assert table.c.error_message.nullable is True
    assert table.c.attempted_at.nullable is True
    assert table.c.sent_at.nullable is True
    assert table.c.created_at.type.fsp == 6
    assert table.c.updated_at.type.fsp == 6
    assert "uq_notifications_provider_message" in _unique_constraint_names(
        "notifications"
    )
    assert _index_names("notifications") == {
        "idx_notifications_inquiry_id",
        "idx_notifications_delivery_status",
        "idx_notifications_created_at",
    }


def test_foreign_keys_use_restrict_deletion_behavior() -> None:
    inquiry_fk = next(iter(Inquiry.__table__.c.customer_id.foreign_keys))
    notification_fk = next(iter(Notification.__table__.c.inquiry_id.foreign_keys))

    assert inquiry_fk.target_fullname == "customers.id"
    assert inquiry_fk.ondelete == "RESTRICT"
    assert notification_fk.target_fullname == "inquiries.id"
    assert notification_fk.ondelete == "RESTRICT"


def test_model_modules_import_without_database_connection() -> None:
    customer = Customer(name="Alex Chen", email="alex@example.com")
    inquiry = Inquiry(customer_id=1, message="Need help with a website.")
    notification = Notification(inquiry_id=1, recipient="owner@example.com")

    assert customer.name == "Alex Chen"
    assert inquiry.message == "Need help with a website."
    assert notification.recipient == "owner@example.com"
