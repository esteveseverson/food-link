from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from food_link.controller.database import get_session
from food_link.middleware.error_hadler import bad_request, forbidden, not_found
from food_link.models.users import User
from food_link.schemas.commom import Message
from food_link.schemas.users import UserCreate, UserList, UserPublic, UserName
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


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session,
    current_user: T_CurrentUser,
    limit: int = 10,
    skip: int = 0,
):
    if current_user.perfil != 'admin':
        raise forbidden(detail='Just admins can see users list')

    users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return {'users': users}

@router.get('/current_user', status_code=HTTPStatus.OK, response_model=UserName)
def get_current_user_name(current_user: T_CurrentUser, session:T_Session):
    
    user = session.query(User).where(User.id == current_user.id).first()
    
    if not user:
        raise not_found(detail='user not found')
    
    return user


@router.get('/{user_id}', response_model=UserPublic)
def get_user_id(session: T_Session, current_user: T_CurrentUser, user_id: int):
    if current_user.perfil != 'admin':
        raise forbidden(detail='Just admins can see users list')

    user_db = session.query(User).where(User.id == user_id).first()

    if not user_db:
        raise not_found(detail='User not found')

    return user_db


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    current_user: T_CurrentUser,
    session: T_Session,
    user_id: int,
    user: UserCreate,
):
    if current_user.id != user_id:
        raise forbidden(detail='Not enough permission')

    # Atualizar os dados do usuário autenticado
    current_user.nome = user.nome
    current_user.cpf = user.cpf
    current_user.email = user.email
    current_user.senha = get_password_hash(user.senha)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/', response_model=Message)
def delete_self_user(current_user: T_CurrentUser, session: T_Session):
    session.delete(current_user)
    session.commit()

    return {'message': 'Seu usuário excluído'}


@router.delete('/{user_id}', response_model=Message)
def delete_other_user(
    current_user: T_CurrentUser, session: T_Session, user_id: int
):
    if current_user.perfil != 'admin':
        raise forbidden(detail='Not enough permission')

    user_db = session.query(User).where(User.id == user_id).first()

    if not user_db:
        raise not_found(detail='User not found')

    session.delete(user_db)
    session.commit()

    return {'message': 'Usuário excluído'}
