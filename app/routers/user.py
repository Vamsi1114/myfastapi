from fastapi import Depends,status,HTTPException,APIRouter,Response
from app import models,database
from ..database import get_db
from app import schemas,oauth2,utils
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=['User'])

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='email_verify')

#create user
@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_account(user : schemas.Create_Account, token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    email_id = oauth2.verify_access_token(token, credential_exception)
    user_data = db.query(models.User).filter(models.User.email_id == email_id.id).first()
    if user_data :
        raise HTTPException(detail= 'user already exists', status_code=status.HTTP_403_FORBIDDEN)
    #hash the password - user.password
    password = user.password.encode('utf-8')
    hashed_password  = utils.hash(password)
    user.password = hashed_password
    new_user = models.User(email_id = email_id.id, **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#change password
@router.put("/change_password")
def change_password(user_credentials : schemas.ChangePassword, current_user: models.User = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user :
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    
    password = user_credentials.password.encode('utf-8')
    hashed_password  = utils.hash(password)
    user.password = hashed_password
    user.updated_on = datetime.now()
    db.commit()
    return {"Meassage" : "password changed sucessfully"}

#forgot password
@router.post("/forgot_password",  response_model=schemas.Token)
def forgot_password(user_credentials : schemas.Email, db : Session = Depends(database.get_db)):
    email = db.query(models.Email).filter(models.Email.email == user_credentials.email).first()
    if email is None:
        raise HTTPException(detail= 'invalid credentials', status_code=status.HTTP_403_FORBIDDEN)
    
    user = db.query(models.User).filter(models.User.email_id == email.id).first()
    if user is None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with email: {user_credentials.email} is not found")
    
    acess_token = oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token" : acess_token, "token_type": "bearer"}

#set password
@router.put("/set_password")
def set_paassword(response : Response, user_credentials : schemas.SetPassword, current_user: models.User = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if user is None:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with email is not found")
    
    password = user_credentials.password.encode('utf-8')
    hashed_password  = utils.hash(password)
    current_user.password = hashed_password
    current_user.updated_on = datetime.now()
    db.commit()
    new_token = "None"
    response.headers.append("new_access_token", new_token)
    return {"Meassage" : "password changed sucessfully"}

#user profile
@router.post("/user_profile", status_code=status.HTTP_201_CREATED)
def user_profile(user: schemas.UserDetails, current_user: models.User = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):
    user_details = db.query(models.UserDetail).filter(models.UserDetail.user_id == current_user.id).first()
    if user_details:
     raise HTTPException(detail= 'user details already exists', status_code=status.HTTP_409_CONFLICT)
      
    data = models.UserDetail(user_id= current_user.id, **user.dict())
    db.add(data)
    db.commit()
    return {"Meassage" : "user profile created sucessfully"}

#edit profile
@router.put("/edit_profile")
def edit_profile(user: schemas.Edit, current_user: models.User = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):
    user_details = db.query(models.UserDetail).filter(models.UserDetail.user_id == current_user.id).first()
    if user_details is None:
        raise HTTPException(detail= 'invalid credentials or user profile was not created', status_code=status.HTTP_403_FORBIDDEN)
    
    copy = user
    for field, value in user.dict(exclude_unset=True).items():
        if value is not None :
            setattr(user_details, field, value)

    user_data = db.query(models.User).filter(models.User.id == current_user.id).first()
    for field, value in copy.dict(exclude_unset=True).items():
        if value is not None :
            setattr(user_data, field , value)

    db.commit()
    return {"Meassage" : "user profile updated sucessfully"}
   

#logout 
@router.post("/logout")
def logout(response : Response, current_user: models.User = Depends(oauth2.get_current_user)):
    new_token = "None"
    response.headers.append("new_access_token", new_token)
    return {"Meassage" : "User logout sucessful"}


