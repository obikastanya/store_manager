from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref
from app import db

class CategoryProduct(db.Model):
    """Object for table ms_category"""
    __tablename__='ms_category'
    msc_id=db.Column(db.Integer(), primary_key=True)
    msc_desc=db.Column(db.String(200))
    msc_active_status=db.Column(db.String(1))
    msc_create_user=db.Column(db.String(30))
    msc_create_date=db.Column(db.Date())
    msc_update_user=db.Column(db.String(30))
    msc_update_date=db.Column(db.Date())
    # relation
    category_product=db.relationship('Product', backref='category_product')

class CategoryProductSchema(Schema):
    """Schema to retrieve data from Model Stock as dictionary.
    data_key is an alias for column name"""
    msc_id=fields.Int(data_key='category_id')
    msc_desc=fields.Str(data_key='category')
    msc_active_status=fields.Str(data_key='active_status')
