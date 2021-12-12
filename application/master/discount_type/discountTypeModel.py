from marshmallow import fields, Schema
from sqlalchemy.orm import relationship
from app import db

class DiscountType(db.Model):
    """Object for table ms_discount_type"""
    __tablename__='ms_discount_type'
    msdt_id=db.Column(db.Integer(), primary_key=True)
    msdt_desc=db.Column(db.String(200))
    msdt_status_aktif=db.Column(db.String(1))
    msdt_create_user=db.Column(db.String(30))
    msdt_create_date=db.Column(db.Date())
    msdt_update_user=db.Column(db.String(30))
    msdt_update_date=db.Column(db.Date())
    discount_type=relationship('ms_discount', backref='ms_discount_type')

class DiscountTypeSchema(Schema):
    """Schema to retrieve data from Model Discount Type as dictionary.
    data_key is an alias for column name."""
    msdt_id=fields.Int(data_key='discount_type_id')
    msdt_desc=fields.Int(data_key='desc')
    msdt_status_aktif=fields.Str(data_key='status_aktif')
