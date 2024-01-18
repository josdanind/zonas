# Standard Library
from typing import Annotated

# FastAPI
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

# CRUDManager
from libraries.CRUDManager import CRUDManager

# Utils
from utils.jwt_manager import authenticate_user, create_access_token

# Database - Databases lib
from config import database_hic_cibus, ACCESS_TOKEN_EXPIRE_DAYS

# Models
from models import crudUserModel

# Schemas
from schemas import Token

router = APIRouter(prefix="/users", tags=["CRUD"])


# **************
# * POST Login *
# **************
@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Login: Obtención del JWT",
    response_model=Token,
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    crud_manager = CRUDManager(database_hic_cibus, crudUserModel)

    user: crudUserModel = await authenticate_user(
        crud_manager, form_data.username, form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user, ACCESS_TOKEN_EXPIRE_DAYS)

    return Token(access_token=access_token, token_type="bearer")
