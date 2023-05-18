from fastapi import FastAPI
from app import models
from .database import engine
from .routers import email,user,auth,pdf


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(email.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(pdf.router)

@app.get("/")
async def root():
    return {"message": "Hello vamsi"}