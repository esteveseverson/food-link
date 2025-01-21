from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from food_link.controller.database import get_session
from food_link.middleware.error_hadler import forbidden
from food_link.models.donation import Donation
from food_link.models.users import User
from food_link.schemas.donation import DonationBase, DonationPublic
from food_link.utils.datetime_transformer import utc_to_datetime
from food_link.validators.security import get_current_user

router = APIRouter(prefix='/donation', tags=['Donation'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=DonationPublic)
def create_doantion(donation: DonationBase, current_user: T_CurrentUser, session: T_Session):
    if current_user.perfil != 'doador':
        raise forbidden(detail='only givers can make a donation')

    new_donation = Donation(
        id_user=current_user.id,
        item=donation.item,
        quantity=donation.quantity,
        street=donation.street,
        number=donation.number,
        neighborhood=donation.neighborhood
    )

    session.add(new_donation)
    session.commit()
    session.refresh(new_donation)
    
    new_donation.created_at = utc_to_datetime(new_donation.created_at)

    return new_donation
