from operator import pos
from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db

class Employee(db.Model):
    """Object for table ms_employee"""
    __tablename__='ms_employee'
    mse_id =db.Column(db.Integer(), primary_key=True)
    msse_id=db.Column(db.Integer())
    mse_name=db.Column(db.String(200))
    mse_phone_number=db.Column(db.String(30))
    mse_email=db.Column(db.String(100))
    mse_address=db.Column(db.String(200))
    mse_salary=db.Column(postgresql.NUMERIC(12))
    mse_position=db.Column(db.String(100))
    mse_start_working=db.Column(db.Date())
    mse_end_working=db.Column(db.Date())
    mse_create_user=db.Column(db.String(30))
    mse_create_date=db.Column(db.Date())
    mse_update_user=db.Column(db.String(30))
    mse_update_date=db.Column(db.Date())

class EmployeeSchema(Schema):
    """Schema to retrieve data from Model Employee as dictionary.
    data_key is an alias for column name."""
    mse_id =fields.Int(data_key='employee_id')
    msse_id=fields.Int(data_key='employee_status')
    mse_name=fields.Str(data_key='name')
    mse_phone_number=fields.Str(data_key='phone_number')
    mse_email=fields.Str(data_key='email')
    mse_address=fields.Str(data_key='address')
    mse_salary=fields.Int(data_key='salary')
    mse_position=fields.Str(data_key='position')
    mse_start_working=fields.Date(data_key='start_working')
    mse_end_working=fields.Date(data_key='end_working')