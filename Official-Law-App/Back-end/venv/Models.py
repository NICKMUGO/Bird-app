from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db=SQLAlchemy(metadata=metadata)


class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer(), primary_key=True, unique=True)
    name=db.Column(db.String)
    email=db.Column(db.String(345), unique=True)
    password=db.Column(db.String, nullable=False)

    @validates('email')
    def validate_email(self,key,address):
        if '@' not in address:
            return ValueError("Invalid Email Address")
        else:
            return address
    @validates('password')
    def validate_password(self,key,size):
        if len(size)<8:
            raise ValueError("Password must be at least 8 characters long.")
        elif not any(char.isdigit() for char in size):
            raise ValueError("Password must contain a number.")
        elif not any(char.islower() for char in size):  
            raise  ValueError("Password must contain a lowercase letter.")
        elif not any(char.isupper() for char in size):
            raise ValueError("Password must contain an uppercase letter.")
            
        return size
        





