from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,Date
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Email(Base):
     __tablename__ = "emails"
     id = Column(Integer, primary_key=True, index=True)
     email = Column(String, nullable=False, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(TIMESTAMP(timezone=True))
    phone_number = Column(String, nullable=False)
    

class UserDetail(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bio = Column(String)
    image_url =  Column(String)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on =  Column(TIMESTAMP(timezone=True))