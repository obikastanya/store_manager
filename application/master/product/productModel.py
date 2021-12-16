from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Product(db.Model):
    """Object for table ms_product"""
    __tablename__='ms_product'
    msp_id =db.Column(db.Integer(), primary_key=True)
    msp_brand=db.Column(db.String(100))
    msp_msc_id=db.Column(db.Integer())
    msp_price =db.Column(postgresql.NUMERIC(12))
    msp_desc=db.Column(db.String(500))
    msp_mssp_id=db.Column(db.Integer())
    msp_mscp_id=db.Column(db.Integer())
    msp_active_status=db.Column(db.String(1))
    msp_create_user=db.Column(db.String(30))
    msp_create_date=db.Column(db.Date())
    msp_update_user=db.Column(db.String(30))
    msp_update_date=db.Column(db.Date())

class ProductSchema(Schema):
    """Schema to retrieve data from Model Product as dictionary.
    data_key is an alias for column name"""
    msp_id =fields.Int(data_key='product_id')
    msp_brand=fields.Str(data_key='brand')
    msp_msc_id=fields.Str(data_ket='category')
    msp_price =fields.Int(data_key='price')
    msp_desc=fields.Str(data_key='desc')
    msp_mssp_id=fields.Str(data_key='supplier')
    msp_mscp_id=fields.Str(data_key='company')
    msp_active_status=fields.Str(data_key='active_status')