from app import schemas
import pytest
from jose import jwt
from app.config import settings
# from .test_database import client,session

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Hello vamsi'
    assert res.status_code == 200

@pytest.mark.parametrize("email , status_code", [('vamsi@gmail.com', 200),('vamsi123@gmail.com', 200)])

#test email 
def test_email(client, email , status_code):
 res = client.post("/email_verify", json= {"email": email})
 token = schemas.Token(**res.json())
 payload = jwt.decode(token.access_token,settings.secret_key,algorithms=[settings.algorithm])
 id : str = payload.get("user_id")
 assert id == 1
 assert res.status_code == status_code
 assert token.token_type == "bearer"

#test the user already existed  email
def test_existed_user_email(client, test_user):
 res = client.post("/email_verify", json= {"email": "vamsi@gmail.com"})
 assert res.status_code == 409

# def test_existed_user_email(client, test_email):
#  res = client.post("/email_verify", json= {"email": "vamsi@gmail.com"})
#  print(res.json())
#  assert res.status_code == 200

#test create user
def test_create_user(authorized_email):
   user_data =  {"first_name" : "krishna", "last_name" : "vamsi", "password": "password", "date_of_birth" : "1999-11-14", "phone_number" : "96758738738"}
   res = authorized_email.post("/user", json= user_data)
   new_user = schemas.UserOut(**res.json())
   assert res.status_code == 201
   assert new_user.first_name == "krishna"

#test unauthorized user to create account
def test_unauthorized_create_user(client):
   user_data =  {"first_name" : "krishna", "last_name" : "vamsi", "password": "password", "date_of_birth" : "1999-11-14", "phone_number" : "96758738738"}
   res = client.post("/user", json= user_data)
   assert res.status_code == 401

# already existed user test
def test_existed_user(authorized_email, test_user):
   res = authorized_email.post("/user", json= test_user)
   assert res.status_code == 409

#login test
def test_login_user(client, test_user):
    res = client.post("/login", data = {"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id : str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200   

@pytest.mark.parametrize("email , password , status_code",[('vamsi12@gmailcom','password123',403),('vamsi@gmailcom','password123',403),('vamsi@gmailcom','password23',403),( None,'password23',422),('vamsi@gmailcom',None,422)])
#test incorrect login details
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    assert res.status_code == status_code

#test change_password
def test_change_password(authorized_client):
   res = authorized_client.put("/change_password", json = {"password": "password", "new_password": "password123"})
   assert res.status_code == 200

#test invalid credentials to change password
def test_change_password_invalid_credentials(authorized_client):
   res = authorized_client.put("/change_password", json = {"password": "password1", "new_password": "password123"})
   assert res.status_code == 403
   
#test unauthorized client to change password
def test_unauthorized_user(client):
   res = client.put("/change_password", json = {"password": "password", "new_password": "password123"})
   assert res.status_code == 401

#test create user profile
def test_user_profile(authorized_client):
   res = authorized_client.post("/user_profile", json= {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
   assert res.status_code == 201

#test user with profile already existed
def test_existed_user_profile(authorized_client, user_profile):
   res = authorized_client.post("/user_profile", json= {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
   assert res.status_code == 409

#unauthorized client to create profile
def test_unauthorized_user_create_profile(client):
    res = client.post("/user_profile", json= {"bio": "cool", "image_url": "img.jpg", "gender": "male", "address":"goa"})
    assert res.status_code == 401

#test edit user details
def test_edit_user_details(authorized_client, user_profile):
   user_data = {
    "first_name" : "vamsi",
    "last_name" : "chinni",
    "date_of_birth" : "1999-11-14",
    "phone_number" : "96758738738",
    "bio": "movie",
    "image_url": "img.png",
    "gender": "male",
    "address":"mvp, vizag"
}
   res = authorized_client.put("/edit_user_details", json = user_data)
   assert res.status_code == 200

#test forgot password
def test_forgot_password(authorized_client, test_user):
   res = authorized_client.post("/forgot_password", json= {"email": test_user["email"]})
   token = schemas.Token(**res.json())
   payload = jwt.decode(token.access_token, settings.secret_key, algorithms= [settings.algorithm])
   id : str = payload.get("user_id")
   assert id == test_user['id']
   assert token.token_type == "bearer"
   assert res.status_code == 200 

#test forgot password with email not existed 
def test_user_forgot_password_email_not_existed(client):
   res = client.post("/forgot_password", json= {"email": "sachin@gmail.com"})
   assert res.status_code == 403 

# test authorized user to set password
def test_authorized_user_set_password(authorized_client):
   res = authorized_client.put("/set_password", json= { "password":"password"})
   assert res.status_code == 200 

#test unauthorized user to set password
def test_unauthorized_user_set_password(client, test_user):
   client.headers["authorization"] = f"Bearer {'None'}"
   res = client.put("/set_password", json= { "password":test_user["password"]})
   assert res.status_code == 401 

#test logout user
def test_logout_user(authorized_client):
   res = authorized_client.post("/logout")
   assert res.json() == {"Meassage" : "User logout sucessful"}
   assert res.status_code == 200 

#test unauthorized user to logout
def test_unauthorized_user_logout(client):
   res = client.post("/logout")
   assert res.status_code == 401 

#test authorized user print userdetails
def test_authorized_user_print_pdf(authorized_client, user_profile):
   res = authorized_client.post("/print")
   data = res.json()
   assert data["filename"] == "example.pdf"
   assert data["file_path"] == "C:\\Users\\CS0142302.CSVIZAG\\Documents\\MyfastAPI2\\example.pdf"
   assert res.status_code == 200

#test unauthorized user to print userdetails 
def test_unauthorized_user_print_pdf(client):
   res = client.post("/print")
   assert res.status_code == 401


