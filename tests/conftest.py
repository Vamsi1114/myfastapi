from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db,Base
import pytest
from app import schemas
from jose import jwt

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Vamsi003@localhost:5432/fastapi_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session) :
    def override_get_db():
     try:
        yield session
     finally:
        session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

#email
@pytest.fixture()
def test_email(client):
 res = client.post("/email_verify", json= {"email": "vamsi@gmail.com"})
 #return we get a token 
 token = schemas.Token(**res.json())
 return token.access_token

#creating a authorized email
@pytest.fixture()
def authorized_email(client, test_email):
   client.headers = {**client.headers,"Authorization":f"Bearer {test_email}"}
   return client

#create a new user
@pytest.fixture()
def test_user(authorized_email):
   user_data =  {"first_name" : "krishna", "last_name" : "vamsi", "password": "password", "date_of_birth" : "1999-11-14", "phone_number" : "96758738738"}
   res = authorized_email.post("/user", json= user_data)
   new_user = res.json()
   new_user['email'] = "vamsi@gmail.com"
   new_user['password'] = user_data["password"]
   return new_user

#user login
@pytest.fixture() 
def test_login_user(client,test_user):
    res = client.post("/login", data = {"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    return login_res.access_token

#authorized user
@pytest.fixture()
def authorized_client(client, test_login_user):
   #client.headers = {**client.headers,"Authorization":f"Bearer {test_login_user}"}
   client.headers["Authorization"] = f"Bearer {test_login_user}"
   return client

#creating a profile 
@pytest.fixture()
def user_profile(authorized_client):
   res = authorized_client.post("/user_profile", json= {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
   new_user_profile = res.json()
   return new_user_profile

