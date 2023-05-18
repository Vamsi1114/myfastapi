from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from app import schemas,models,database,oauth2

router = APIRouter(tags=['Email_verify'])

@router.post('/email_verify', response_model=schemas.Token)
def email_verify(email : schemas.Email, db : Session = Depends(database.get_db)):

    data = db.query(models.Email).filter(models.Email.email == email.email).first()
    if data is None:
     new_email = models.Email(**email.dict())
     db.add(new_email)
     db.commit()

    email_data = db.query(models.Email).filter(models.Email.email == email.email).first()
    user = db.query(models.User).filter(models.User.email_id == email_data.id).first()
    if user  :
      raise HTTPException(detail= 'user already exists', status_code=status.HTTP_403_FORBIDDEN)
    
    acess_token = oauth2.create_access_token(data={"user_id":email_data.id})
    return {"access_token" : acess_token, "token_type": "bearer"}