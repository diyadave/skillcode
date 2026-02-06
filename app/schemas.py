from pydantic import BaseModel

class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str
    message: str
