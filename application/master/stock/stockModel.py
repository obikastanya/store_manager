from enum import unique
from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Stock(db.Model):
    """Object for table ms_stock"""
    __tablename__='ms_stock'
    mss_id=db.Column(db.Integer(), primary_key=True)
    mss_msp_id=db.Column(db.Integer(), db.ForeignKey('ms_product.msp_id'), unique=True)
    mss_warehouse_stock=db.Column(postgresql.NUMERIC(8))
    mss_store_stock=db.Column(postgresql.NUMERIC(8))
    mss_create_user=db.Column(db.String(30))
    mss_create_date=db.Column(db.Date())
    mss_update_user=db.Column(db.String(30))
    mss_update_date=db.Column(db.Date())

class StockSchema(Schema):
    
    """Schema to retrieve data from Model Stock as dictionary.
    data_key is an alias for column name"""
    mss_id=fields.Int(data_key='stock_id')
    mss_warehouse_stock=fields.Int(data_key='warehouse_stock')
    mss_store_stock=fields.Int(data_key='store_stock')
    product=fields.Nested('ProductSchema',only=('msp_id','msp_desc'))
