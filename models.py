from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum

class location(Enum):
    JC2 = "Johnson Center 2"
    JC3 = "Johnson Center 3"
    Fen2 = "Fenwick 2"
    Fen3 = "Fenwick 3"
    Fen4 = "Fenwick 4"


db = SQLAlchemy()



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) 
    loc = db.Column(db.String(50), default="JC3")