# Standard Library
from datetime import datetime, timedelta
import json
from typing import Annotated

# FastAPI
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Utils
from utils.encrypt import context
from utils.console_message import crud_error_message

# Config
from config import SECRET_KEY, ALGORITHM, database_hic_cibus


# pyJWT
import jwt
from jwt import DecodeError, ExpiredSignatureError

# Schemas
from schemas import TokenData

# models
from models import crudUserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

credentials_exception = lambda msg: HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    # detail="Could not validate credentials",
    detail=msg,
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(user: crudUserModel, expire_days: int | None = None):
    if expire_days:
        expire = timedelta(days=expire_days)
    else:
        expire = timedelta(minutes=15)

    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + expire,
        "scopes": json.loads(user.data)["scopes"],
        "sub": user.id,
        "username": user.username,
    }

    return jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(crud_manager: CRUDManager, username: str, password: str):
    user: crudUserModel = await crud_manager.verify_existence(username=username)

    if not user:
        return False
    if not context.verify(password, user.hashed_password):
        return False

    return user


async def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload: dict = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload["sub"]
        username: str = payload["username"]

        if user_id is None:
            raise credentials_exception("Could not validate credentials")

        return TokenData(id=user_id, username=username, scopes=payload["scopes"])
    except DecodeError:
        crud_error_message("Error decoding token")
    except ExpiredSignatureError:
        crud_error_message("Token has expired")
        raise credentials_exception("Token has expired")


async def user_authorization(
    token_data: Annotated[TokenData, Depends(decode_access_token)]
):
    crud_manager = CRUDManager(database_hic_cibus, crudUserModel)
    user = await crud_manager.verify_existence(id=token_data.id)

    if user is None:
        raise credentials_exception("Could not validate credentials")

    return user
