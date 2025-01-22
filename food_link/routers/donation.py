from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from food_link.controller.database import get_session
from food_link.middleware.error_hadler import bad_request, forbidden, not_found
from food_link.models.donation import Donation
from food_link.models.users import User
from food_link.schemas.commom import Message
from food_link.schemas.donation import (
    DonationBase,
    DonationList,
    DonationPublic,
    DonationUpdate,
)
from food_link.utils.datetime_transformer import utc_to_datetime
from food_link.validators.security import get_current_user

router = APIRouter(prefix='/donation', tags=['Donation'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=DonationPublic)
def create_donation(donation: DonationBase, current_user: T_CurrentUser, session: T_Session):
    if current_user.perfil != 'doador':
        raise forbidden(detail='only givers can make a donation')

    if donation.quantity <= 0:
        raise bad_request(detail='input a valid quantity')

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


@router.get('/', status_code=HTTPStatus.OK, response_model=DonationList)
def read_donations(current_user: T_CurrentUser, session: T_Session, limit: int = 10, skip: int = 0):

    donations = session.scalars(select(Donation).limit(limit).offset(skip)).all()
    for donation in donations:
        donation.created_at = utc_to_datetime(donation.created_at)

    return {'donations': donations}


@router.patch('/{donation_id}', response_model=DonationPublic)
def update_donation(
    donation_id: int,
    current_user: T_CurrentUser,
    session: T_Session,
    donation: DonationUpdate
):
    db_donation = session.scalar(
        select(Donation).where(Donation.id == donation_id)
    )

    if not db_donation:
        raise not_found(detail='donation not found')

    for key, value in donation.model_dump(exclude_unset=True).items():
        setattr(db_donation, key, value)

    session.add(db_donation)
    session.commit()
    session.refresh(db_donation)

    db_donation.created_at = utc_to_datetime(db_donation.created_at)

    return db_donation


@router.delete('/{donation_id}', response_class=Message)
def delete_user(current_user: T_CurrentUser, session: T_Session, donation_id: int):
    if current_user.perfil != 'admin':
        raise forbidden(detail='only admins can delete users')

    donation_db = session.query(Donation).where(Donation.id == donation_id).first()

    if not donation_db:
        raise not_found(detail='User not found')

    session.delete(donation_db)
    session.commit()

    return {'message': 'donation excluded'}
