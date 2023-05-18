from fastapi import APIRouter, Depends, status,HTTPException,Response
from sqlalchemy.orm import Session
from .. import database , schemas, models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])
#login router or path operation 
@router.post('/login', response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
   
   user = db.query(models.User, models.Email).join(models.Email, models.User.email_id == models.Email.id).filter(models.Email.email == user_credentials.username, models.User.email_id == models.Email.id).add_columns(models.User.id, models.User.password, models.Email.id, models.Email.email).first()
   if not user :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
 
   if not utils.verify(user_credentials.password, user.password):
       raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
   
   #we create a token 
   acess_token = oauth2.create_access_token(data={"user_id":user.id})
   # return the token
   return {"access_token" : acess_token, "token_type": "bearer"}

















#    user = db.query(models.User, models.Email).join(models.Email, models.User.email_id == models.Email.id).filter(models.Email.email == user_credentials.username, models.User.email_id == models.Email.id ).first()