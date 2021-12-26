from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Company(db.Model):
    """Object for table ms_company"""
    __tablename__='ms_company'
    mscp_id=db.Column(db.Integer(), primary_key=True)
    mscp_desc=db.Column(db.String(200))
    mscp_active_status=db.Column(db.String(1))
    mscp_create_user=db.Column(db.String(30))
    mscp_create_date=db.Column(db.Date())
    mscp_update_user=db.Column(db.String(30))
    mscp_update_date=db.Column(db.Date())
    # relationship
    company=db.relationship('Product', backref='company')

class CompanySchema(Schema):
    """Schema to retrieve data from Model Company as dictionary.
    data_key is an alias for column name"""
    mscp_id=fields.Int(data_key='company_id')
    mscp_desc=fields.Str(data_key='company')
    mscp_active_status=fields.Str(data_key='active_status')
