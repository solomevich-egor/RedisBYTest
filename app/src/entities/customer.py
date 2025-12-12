from pydantic import BaseModel


class PhoneNumber(BaseModel):
    number: str


class Customer(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: str
    phones: list[PhoneNumber]
    created_at: str | None = None
    site: str | None = None
