"""create initial inquiry schema

Revision ID: 20260721_0001
Revises:
Create Date: 2026-07-21

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = "20260721_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column(
            "id",
            mysql.BIGINT(unsigned=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", mysql.VARCHAR(length=120), nullable=False),
        sa.Column("email", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("phone", mysql.VARCHAR(length=50), nullable=True),
        sa.Column("company", mysql.VARCHAR(length=160), nullable=True),
        sa.Column(
            "preferred_contact_method",
            mysql.ENUM("email", "phone"),
            server_default=sa.text("'email'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text("CURRENT_TIMESTAMP(6)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text(
                "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_customers_email"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    op.create_table(
        "inquiries",
        sa.Column(
            "id",
            mysql.BIGINT(unsigned=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("customer_id", mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column("inquiry_type", mysql.VARCHAR(length=80), nullable=True),
        sa.Column("budget_range", mysql.VARCHAR(length=80), nullable=True),
        sa.Column("timeline", mysql.VARCHAR(length=120), nullable=True),
        sa.Column("message", mysql.TEXT(), nullable=False),
        sa.Column(
            "status",
            mysql.ENUM("new", "in_progress", "completed", "archived"),
            server_default=sa.text("'new'"),
            nullable=False,
        ),
        sa.Column("ai_summary", mysql.TEXT(), nullable=True),
        sa.Column("ai_customer_need", mysql.TEXT(), nullable=True),
        sa.Column(
            "ai_urgency",
            mysql.ENUM("low", "medium", "high", "unknown"),
            nullable=True,
        ),
        sa.Column("ai_missing_information", mysql.TEXT(), nullable=True),
        sa.Column("ai_suggested_next_action", mysql.TEXT(), nullable=True),
        sa.Column("ai_generated_at", mysql.DATETIME(fsp=6), nullable=True),
        sa.Column(
            "ai_generation_status",
            mysql.ENUM("pending", "succeeded", "failed"),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("ai_generation_error", mysql.TEXT(), nullable=True),
        sa.Column(
            "created_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text("CURRENT_TIMESTAMP(6)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text(
                "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index(
        "idx_inquiries_ai_generation_status",
        "inquiries",
        ["ai_generation_status"],
    )
    op.create_index("idx_inquiries_created_at", "inquiries", ["created_at"])
    op.create_index("idx_inquiries_customer_id", "inquiries", ["customer_id"])
    op.create_index(
        "idx_inquiries_status_created_at",
        "inquiries",
        ["status", "created_at"],
    )

    op.create_table(
        "notifications",
        sa.Column(
            "id",
            mysql.BIGINT(unsigned=True),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("inquiry_id", mysql.BIGINT(unsigned=True), nullable=False),
        sa.Column(
            "notification_type",
            mysql.VARCHAR(length=80),
            server_default=sa.text("'new_inquiry'"),
            nullable=False,
        ),
        sa.Column(
            "channel",
            mysql.VARCHAR(length=40),
            server_default=sa.text("'email'"),
            nullable=False,
        ),
        sa.Column("recipient", mysql.VARCHAR(length=255), nullable=False),
        sa.Column(
            "delivery_status",
            mysql.ENUM("pending", "sent", "failed"),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("provider_name", mysql.VARCHAR(length=80), nullable=True),
        sa.Column(
            "provider_message_id",
            mysql.VARCHAR(length=255),
            nullable=True,
        ),
        sa.Column("error_message", mysql.TEXT(), nullable=True),
        sa.Column("attempted_at", mysql.DATETIME(fsp=6), nullable=True),
        sa.Column("sent_at", mysql.DATETIME(fsp=6), nullable=True),
        sa.Column(
            "created_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text("CURRENT_TIMESTAMP(6)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text(
                "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["inquiry_id"],
            ["inquiries.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "provider_name",
            "provider_message_id",
            name="uq_notifications_provider_message",
        ),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index(
        "idx_notifications_created_at",
        "notifications",
        ["created_at"],
    )
    op.create_index(
        "idx_notifications_delivery_status",
        "notifications",
        ["delivery_status"],
    )
    op.create_index(
        "idx_notifications_inquiry_id",
        "notifications",
        ["inquiry_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_notifications_inquiry_id", table_name="notifications")
    op.drop_index("idx_notifications_delivery_status", table_name="notifications")
    op.drop_index("idx_notifications_created_at", table_name="notifications")
    op.drop_table("notifications")

    op.drop_index("idx_inquiries_status_created_at", table_name="inquiries")
    op.drop_index("idx_inquiries_customer_id", table_name="inquiries")
    op.drop_index("idx_inquiries_created_at", table_name="inquiries")
    op.drop_index("idx_inquiries_ai_generation_status", table_name="inquiries")
    op.drop_table("inquiries")

    op.drop_table("customers")

