from datetime import datetime

from pydantic import BaseModel


class DonationBase(BaseModel):
    item: str
    quantity: int
    street: str
    number: int
    neighborhood: str


class DonationPublic(BaseModel):
    id: int
    id_user: int
    item: str
    quantity: int
    street: str
    number: int
    neighborhood: str
    created_at: str
