from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from food_link.controller.database import get_session
from food_link.middleware.error_hadler import bad_request
from food_link.models.users import User
from food_link.schemas.users import UserCreate, UserPublic
from food_link.validators.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['Usuários'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserCreate, session: T_Session):
    # Verifica se CPF ou email já existe
    db_user = session.scalar(
        select(User).where((User.cpf == user.cpf) | (User.email == user.email))
    )

    if db_user:
        if db_user.cpf == user.cpf:
            raise bad_request(detail='CPF already exists')

        if db_user.email == user.email:
            raise bad_request(detail='Email already exists')

    # Criação do usuário
    db_user = User(
        nome=user.nome,
        cpf=user.cpf,
        email=user.email,
        perfil=user.perfil,
        senha=get_password_hash(user.senha),  # Hash da senha
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
