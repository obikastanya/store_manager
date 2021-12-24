from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Supplier(db.Model):
    """Object for table ms_supplier"""
    __tablename__='ms_supplier'
    mssp_id=db.Column(db.Integer(), primary_key=True)
    mssp_desc=db.Column(db.String(200))
    mssp_phone_number=db.Column(db.String(15))
    mssp_address=db.Column(db.String(300))
    mssp_active_status=db.Column(db.String(1))
    mssp_create_user=db.Column(db.String(30))
    mssp_create_date=db.Column(db.Date())
    mssp_update_user=db.Column(db.String(30))
    mssp_update_date=db.Column(db.Date())

class SupplierSchema(Schema):
    """Schema to retrieve data from Model Supplier as dictionary.
    data_key is an alias for column name."""
    mssp_id=fields.Int(data_key='supplier_id')
    mssp_desc=fields.Str(data_key='supplier')
    mssp_phone_number=fields.Str(data_key='phone_number')
    mssp_address=fields.Str(data_key='address')
    mssp_active_status=fields.Str(data_key='active_status')
