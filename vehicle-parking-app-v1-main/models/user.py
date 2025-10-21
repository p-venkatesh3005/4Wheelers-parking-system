from . import db

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)
    name=db.Column(db.String(50),nullable=False,default='User')