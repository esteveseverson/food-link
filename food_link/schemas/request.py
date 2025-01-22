from pydantic import BaseModel

from food_link.models.request import RequestStatus

class RequestCreate(BaseModel):
    id_donation: int
    id_giver: int
    item: str
    quantity: int

class RequestPublic(BaseModel):
    id: int
    id_donation: int
    id_giver: int
    id_receiver: int
    item: str
    quantity: str
    status: RequestStatus
    order_at: str