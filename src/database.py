from datetime import  datetime
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),unique=True, nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.now())
    updated_at= db.Column(db.DateTime,onupdate=datetime.now())
    tasks=db.relationship("Tasks",backref="user")
    
    
    def __repr__(self) -> str:
        return 'User >>> {self.username}'
    
    
class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body= db.Column(db.Text,nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at= db.Column(db.DateTime,onupdate=datetime.now())
    
    
    def __repr__(self) -> str:
        return 'Tasks>>>{self.body}'
    