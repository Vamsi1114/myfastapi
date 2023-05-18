from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas, database,models
from fastapi import Depends,status, HTTPException,Response
from fastapi.security import OAuth2PasswordBearer
from  sqlalchemy.orm import Session
from .config import settings

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
   to_encode = data.copy()

   expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"exp": expire}) 

   encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

   return encoded_jwt

def verify_access_token (token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

        id : str = payload.get("user_id")

        if id is None:
         raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
       raise credentials_exception
    return token_data
   
def check_and_create_new_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        old_token_expiration = datetime.utcfromtimestamp(payload["exp"])
        current_time = datetime.utcnow()
        time_difference = old_token_expiration - current_time

        if time_difference.total_seconds() < (ACCESS_TOKEN_EXPIRE_MINUTES * 60)/2:
            
            # The old token is close to expiring, create a new token
            new_token_data = {"user_id": payload.get("user_id")}
            new_token = create_access_token(new_token_data)
            return new_token

    except JWTError:
        credential_exception

def get_current_user(response : Response , token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
   credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
   tkn = verify_access_token(token, credential_exception )

   new_tkn = check_and_create_new_token(token, credential_exception)
   if new_tkn:
        response.headers.append("new_access_token", new_tkn)

   user =  db.query(models.User).filter(models.User.id == tkn.id).first()
   if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
   return user