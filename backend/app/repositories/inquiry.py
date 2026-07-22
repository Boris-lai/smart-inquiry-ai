from sqlalchemy.orm import Session

from app.models.inquiry import Inquiry


def add_inquiry(db: Session, inquiry: Inquiry) -> Inquiry:
    db.add(inquiry)
    return inquiry

