from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


BACKEND_DIR = Path(__file__).resolve().parents[1]
REVISION_PATH = (
    BACKEND_DIR
    / "alembic"
    / "versions"
    / "20260721_0001_create_initial_inquiry_schema.py"
)


def test_alembic_has_single_initial_revision() -> None:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    script = ScriptDirectory.from_config(config)
    heads = script.get_heads()

    assert heads == ["20260721_0001"]


def test_initial_migration_contains_approved_schema_markers() -> None:
    migration = REVISION_PATH.read_text()

    assert 'revision: str = "20260721_0001"' in migration
    assert 'op.create_table(\n        "customers"' in migration
    assert 'op.create_table(\n        "inquiries"' in migration
    assert 'op.create_table(\n        "notifications"' in migration
    assert 'mysql.BIGINT(unsigned=True)' in migration
    assert 'mysql.DATETIME(fsp=6)' in migration
    assert 'ondelete="RESTRICT"' in migration
    assert "uq_customers_email" in migration
    assert "uq_notifications_provider_message" in migration
    assert "idx_inquiries_customer_id" in migration
    assert "idx_inquiries_status_created_at" in migration
    assert "idx_inquiries_created_at" in migration
    assert "idx_inquiries_ai_generation_status" in migration
    assert "idx_notifications_inquiry_id" in migration
    assert "idx_notifications_delivery_status" in migration
    assert "idx_notifications_created_at" in migration
    assert "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)" in migration
    assert "attachments" not in migration


def test_initial_migration_drops_tables_in_reverse_dependency_order() -> None:
    migration = REVISION_PATH.read_text()

    notification_drop = migration.index('op.drop_table("notifications")')
    inquiry_drop = migration.index('op.drop_table("inquiries")')
    customer_drop = migration.index('op.drop_table("customers")')

    assert notification_drop < inquiry_drop < customer_drop

