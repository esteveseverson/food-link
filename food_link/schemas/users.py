from typing import List

from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict

from food_link.models.users import PerfilUsuario


class UserBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: PerfilUsuario


class UserCreate(UserBase):
    senha: str
    cpf: str


class UserPublic(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserPublic]


class UserName(BaseModel):
    nome: str
