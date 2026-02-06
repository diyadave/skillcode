from sqlalchemy.orm import Session
from .models import ContactMessage
from .schemas import ContactCreate

def create_contact(db: Session, data: ContactCreate):
    contact = ContactMessage(
        name=data.name,
        email=data.email,
        subject=data.subject,
        message=data.message
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
