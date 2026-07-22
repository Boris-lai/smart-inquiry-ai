from collections.abc import Callable

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import APIError
from app.models.customer import Customer
from app.models.enums import AIGenerationStatus, InquiryStatus, PreferredContactMethod
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreateRequest
from app.services import inquiry as inquiry_service


class FakeSession:
    def __init__(
        self,
        *,
        customers: dict[str, Customer] | None = None,
        fail_on_flush_number: int | None = None,
    ) -> None:
        self.customers = customers or {}
        self.added_customers: list[Customer] = []
        self.added_inquiries: list[Inquiry] = []
        self.events: list[str] = []
        self.flush_count = 0
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_on_flush_number = fail_on_flush_number

    def flush(self) -> None:
        self.flush_count += 1
        self.events.append("flush")
        if self.fail_on_flush_number == self.flush_count:
            raise SQLAlchemyError("driver detail that must stay private")

        for customer in self.added_customers:
            if customer.id is None:
                customer.id = 12
        for inquiry in self.added_inquiries:
            if inquiry.id is None:
                inquiry.id = 101

    def commit(self) -> None:
        self.events.append("commit")
        self.commit_count += 1

    def rollback(self) -> None:
        self.events.append("rollback")
        self.rollback_count += 1


def _request(**overrides: object) -> InquiryCreateRequest:
    data = {
        "name": "Alex Chen",
        "email": " Alex@Example.COM ",
        "phone": "+886912345678",
        "company": "Northstar Studio",
        "preferred_contact_method": "email",
        "inquiry_type": "website redesign",
        "budget_range": "100000-200000 TWD",
        "timeline": "within 2 months",
        "message": "We need help redesigning our website.",
    }
    data.update(overrides)
    return InquiryCreateRequest.model_validate(data)


@pytest.fixture(autouse=True)
def patch_repositories(monkeypatch: pytest.MonkeyPatch) -> None:
    def get_customer_by_email(db: FakeSession, email: str) -> Customer | None:
        db.events.append(f"lookup:{email}")
        return db.customers.get(email)

    def add_customer(db: FakeSession, customer: Customer) -> Customer:
        db.events.append("add_customer")
        db.customers[customer.email] = customer
        db.added_customers.append(customer)
        return customer

    def add_inquiry(db: FakeSession, inquiry: Inquiry) -> Inquiry:
        db.events.append("add_inquiry")
        db.added_inquiries.append(inquiry)
        return inquiry

    monkeypatch.setattr(
        inquiry_service.customer_repository,
        "get_customer_by_email",
        get_customer_by_email,
    )
    monkeypatch.setattr(
        inquiry_service.customer_repository,
        "add_customer",
        add_customer,
    )
    monkeypatch.setattr(
        inquiry_service.inquiry_repository,
        "add_inquiry",
        add_inquiry,
    )


def test_new_normalized_email_creates_customer_and_inquiry() -> None:
    db = FakeSession()

    result = inquiry_service.submit_public_inquiry(db, _request())

    customer = db.added_customers[0]
    inquiry = db.added_inquiries[0]
    assert db.events == [
        "lookup:alex@example.com",
        "add_customer",
        "flush",
        "add_inquiry",
        "flush",
        "commit",
    ]
    assert customer.name == "Alex Chen"
    assert customer.email == "alex@example.com"
    assert customer.phone == "+886912345678"
    assert customer.company == "Northstar Studio"
    assert customer.preferred_contact_method == PreferredContactMethod.EMAIL
    assert inquiry.customer_id == 12
    assert inquiry.inquiry_type == "website redesign"
    assert inquiry.budget_range == "100000-200000 TWD"
    assert inquiry.timeline == "within 2 months"
    assert inquiry.message == "We need help redesigning our website."
    assert inquiry.status == InquiryStatus.NEW
    assert inquiry.ai_generation_status == AIGenerationStatus.PENDING
    assert result.inquiry_id == 101


def test_customer_and_inquiry_are_committed_together_after_flush() -> None:
    db = FakeSession()

    result = inquiry_service.submit_public_inquiry(db, _request())

    assert db.commit_count == 1
    assert db.rollback_count == 0
    assert db.flush_count == 2
    assert db.events.index("flush") < db.events.index("commit")
    assert result.status == InquiryStatus.NEW
    assert result.ai_generation_status == AIGenerationStatus.PENDING
    assert result.message == "Your inquiry was received successfully."


def test_existing_customer_is_reused_and_non_null_values_update() -> None:
    existing = Customer(
        id=44,
        name="Old Name",
        email="alex@example.com",
        phone="+111",
        company="Old Company",
        preferred_contact_method=PreferredContactMethod.EMAIL,
    )
    db = FakeSession(customers={"alex@example.com": existing})

    inquiry_service.submit_public_inquiry(
        db,
        _request(
            name="New Name",
            phone="+222",
            company="New Company",
            preferred_contact_method="phone",
        ),
    )

    inquiry = db.added_inquiries[0]
    assert db.added_customers == []
    assert existing.name == "New Name"
    assert existing.phone == "+222"
    assert existing.company == "New Company"
    assert existing.preferred_contact_method == PreferredContactMethod.PHONE
    assert inquiry.customer_id == 44


def test_null_optional_values_do_not_erase_existing_customer_data() -> None:
    existing = Customer(
        id=44,
        name="Old Name",
        email="alex@example.com",
        phone="+111",
        company="Old Company",
        preferred_contact_method=PreferredContactMethod.PHONE,
    )
    db = FakeSession(customers={"alex@example.com": existing})
    request = InquiryCreateRequest.model_validate(
        {
            "name": "Alex Chen",
            "email": " Alex@Example.COM ",
            "phone": " ",
            "company": "",
            "message": "We need help redesigning our website.",
        }
    )

    inquiry_service.submit_public_inquiry(db, request)

    assert existing.phone == "+111"
    assert existing.company == "Old Company"
    assert existing.preferred_contact_method == PreferredContactMethod.PHONE


def test_omitted_preferred_contact_method_does_not_overwrite_existing_customer() -> None:
    existing = Customer(
        id=44,
        name="Old Name",
        email="alex@example.com",
        phone="+111",
        company="Old Company",
        preferred_contact_method=PreferredContactMethod.PHONE,
    )
    db = FakeSession(customers={"alex@example.com": existing})
    request = _request()
    request = InquiryCreateRequest.model_validate(
        request.model_dump(exclude={"preferred_contact_method"})
    )

    inquiry_service.submit_public_inquiry(db, request)

    assert request.preferred_contact_method == PreferredContactMethod.EMAIL
    assert "preferred_contact_method" not in request.model_fields_set
    assert existing.preferred_contact_method == PreferredContactMethod.PHONE


def test_explicit_preferred_contact_method_updates_existing_customer() -> None:
    existing = Customer(
        id=44,
        name="Old Name",
        email="alex@example.com",
        phone="+111",
        company="Old Company",
        preferred_contact_method=PreferredContactMethod.PHONE,
    )
    db = FakeSession(customers={"alex@example.com": existing})

    inquiry_service.submit_public_inquiry(
        db,
        _request(preferred_contact_method="email"),
    )

    assert existing.preferred_contact_method == PreferredContactMethod.EMAIL


def test_write_failure_rolls_back_and_does_not_commit() -> None:
    existing = Customer(
        id=44,
        name="Old Name",
        email="alex@example.com",
        preferred_contact_method=PreferredContactMethod.EMAIL,
    )
    db = FakeSession(
        customers={"alex@example.com": existing},
        fail_on_flush_number=1,
    )

    with pytest.raises(APIError) as exc_info:
        inquiry_service.submit_public_inquiry(db, _request())

    assert exc_info.value.status_code == 500
    assert db.rollback_count == 1
    assert db.commit_count == 0
    assert db.events[-1] == "rollback"


def test_no_notification_or_ai_or_email_work_is_performed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = FakeSession()
    blocked_names = ["create_notification", "send_email", "generate_ai"]

    for name in blocked_names:
        monkeypatch.setattr(
            inquiry_service,
            name,
            _fail_if_called(name),
            raising=False,
        )

    inquiry_service.submit_public_inquiry(db, _request())

    inquiry = db.added_inquiries[0]
    assert not hasattr(db, "added_notifications")
    assert inquiry.ai_summary is None
    assert inquiry.ai_customer_need is None
    assert inquiry.ai_urgency is None
    assert inquiry.ai_missing_information is None
    assert inquiry.ai_suggested_next_action is None
    assert inquiry.ai_generated_at is None
    assert inquiry.ai_generation_error is None


def _fail_if_called(name: str) -> Callable[..., None]:
    def fail(*_args: object, **_kwargs: object) -> None:
        raise AssertionError(f"{name} should not be called")

    return fail
