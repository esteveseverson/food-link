from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from food_link.controller.registry import table_registry


@table_registry.mapped_as_dataclass
class Donation:
    __tablename__ = 'donation'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    item: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    neighborhood: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
