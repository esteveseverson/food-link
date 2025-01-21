from typing import List

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


class DonationList(BaseModel):
    donations: List[DonationPublic]
    
class DonationUpdate(BaseModel):
    item: str | None = None
    quantity: int | None = None
    street: str | None = None
    number: int | None = None
    neighborhood: str | None = None
