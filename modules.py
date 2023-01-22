from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INTEGER, Column, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



sesion=sessionmaker()

db=SQLAlchemy()

Base=declarative_base()

engine=create_engine('postgresql+psycopg2://postgres:dannewton\
@localhost/gold')

class User(db.Model,UserMixin):
    __tablename__='user'
    id=Column(INTEGER(),primary_key=True)
    username=Column(String(30),nullable=False,unique=True)
    password=Column(String(300),nullable=False,unique=True)

