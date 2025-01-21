from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from food_link.routers import auth, donation, users

app = FastAPI()

origins = [
    'http://localhost:3000',
    'http://localhost:4200',
    '192.168.15.164:4200'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(donation.router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Food Link API  --- go to /docs to see the swager'}
