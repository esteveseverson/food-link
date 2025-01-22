from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from food_link.controller.registry import table_registry

class RequestStatus(str, Enum):
    pending = 'pending'
    approved = 'approved'
    denied = 'denied'
    


@table_registry.mapped_as_dataclass
class Request:
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_donation: Mapped[int] = mapped_column(ForeignKey('donation.id'))
    id_giver: Mapped[int] = mapped_column(ForeignKey('donation.id_user'))
    id_receiver: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[RequestStatus] = mapped_column(nullable=False)

    order_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
