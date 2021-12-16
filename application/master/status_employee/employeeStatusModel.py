from marshmallow import fields, Schema
from app import db

class StatusEmployee(db.Model):
    """Object for table ms_status_employee"""
    __tablename__='ms_status_employee'
    msse_id =db.Column(db.Integer(), primary_key=True)
    msse_desc=db.Column(db.String(200))
    msse_active_status=db.Column(db.String(1))
    msse_create_user=db.Column(db.String(30))
    msse_create_date=db.Column(db.Date())
    msse_update_user=db.Column(db.String(30))
    msse_update_date=db.Column(db.Date())

class StatusEmployeeSchema(Schema):
    """Schema to retrieve data from Model Product as dictionary.
    data_key is an alias for column name"""
    msse_id =fields.Str(data_key='employee_status_id')
    msse_desc=fields.Str(data_key='employee_status')
    msse_active_status=fields.Str(data_key='active_status')