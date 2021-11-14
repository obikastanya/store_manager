from marshmallow import fields, Schema
from app import db

class User(db.Model):
    __tablename__='tb_user'
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(128))

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()
