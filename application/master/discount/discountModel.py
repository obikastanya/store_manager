from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Discount(db.Model):
    """Object for table ms_stock"""
    __tablename__='ms_discount'
    msd_id=db.Column(db.Integer(), primary_key=True)
    msd_msdt_id=db.Column(db.Integer())
    msd_desc=db.Column(db.String(150))
    msd_nominal=db.Column(postgresql.NUMERIC(12))
    msd_status_aktif=db.Column(db.String(1))
    msd_create_user=db.Column(db.String(30))
    msd_create_date=db.Column(db.Date())
    msd_update_user=db.Column(db.String(30))
    msd_update_date=db.Column(db.Date())

class DiscountSchema(Schema):
    """Schema to retrieve data from Model Stock as dictionary.
    data_key is an alias for column name"""
    msd_id=fields.Int(data_key='discount_id')
    msd_msdt_id=fields.Int(data_key='discount_type_id')
    msd_desc=fields.Str(data_key='desc')
    msd_nominal=fields.Int(data_key='nominal_discount')
    msd_status_aktif=fields.Int(data_key='status_aktif')