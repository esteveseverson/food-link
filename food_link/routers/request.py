from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from food_link.controller.database import get_session
from food_link.models.users import User
from food_link.middleware.error_hadler import forbidden, bad_request
from food_link.models.request import Request
from food_link.schemas.request import RequestCreate, RequestPublic
from food_link.utils.datetime_transformer import utc_to_datetime
from food_link.validators.security import get_current_user


router = APIRouter(prefix='/request', tags=['Request'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', status_code=HTTPStatus.CREATED, response_model=RequestPublic)
def create_request(request: RequestCreate, current_user: T_CurrentUser, session: T_Session):
    if current_user.perfil != 'beneficiario':
        raise forbidden(detail='only needys can ask for a donate')
    
    if request.quantity <= 0:
        raise bad_request(detail='input a valid quantity')
    
    new_request = Request(
        id_donation= request.id_donation,
        id_giver=request.id_giver,
        id_receiver=current_user.id,
        item=request.item,
        quantity=request.quantity,
        status='pending'
    )
    
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    
    new_request.order_at = utc_to_datetime(new_request.order_at)
    
    return new_request