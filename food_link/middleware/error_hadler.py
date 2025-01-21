from http import HTTPStatus

from fastapi import HTTPException


def credentials_exception():
    error_credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    return error_credentials_exception


def bad_request(detail: str):
    error_bad_request = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail=detail
    )

    return error_bad_request
