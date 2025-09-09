from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenURL="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    pass