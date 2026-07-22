from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_customer_by_email(db: Session, email: str) -> Customer | None:
    statement = select(Customer).where(Customer.email == email)
    return db.scalar(statement)


def add_customer(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    return customer

