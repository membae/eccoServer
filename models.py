from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model,SerializerMixin):
    __tablename__="users"
    
    id=db.Column(db.Integer, primary_key=True)
    full_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, unique=True, nullable=False)
    phone_number=db.Column(db.Integer, nullable=False)
    country=db.Column(db.String, nullable=False)
    role=db.Column(db.String, default="user", nullable=False)