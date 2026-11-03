from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    email: EmailStr
