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
    phone_number=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    country=db.Column(db.String, nullable=False)
    role=db.Column(db.String, default="user", nullable=False)
    
    balance = db.relationship('Balance', back_populates='user', uselist=False, cascade="all, delete-orphan")
    
    serialize_rules = ("-balance.user",)
    
class Balance(db.Model,SerializerMixin):
    __tablename__="balances"
    
    id=db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    user = db.relationship('User', back_populates='balance')
    
    serialize_rules = ("-user.balance",)
    
class Wallet(db.Model, SerializerMixin):
    __tablename__="wallets"
    
    id=db.Column(db.Integer, primary_key=True)
    wallet=db.Column(db.String, nullable=False)