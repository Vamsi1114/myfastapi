from app.calac import add
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from jose import jwt
from app.config import settings

client = TestClient(app)

def test_add():
 print("testing add function")
 sum = add(5,3)
 assert sum == 8




