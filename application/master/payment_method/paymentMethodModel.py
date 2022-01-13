from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref
from app import db

class PaymentMethod(db.Model):
    """Object for table ms_stock"""
    __tablename__='ms_payment_method'
    mspm_id=db.Column(db.Integer(), primary_key=True)
    mspm_desc=db.Column(db.String(200))
    mspm_active_status=db.Column(db.String(1))
    mspm_create_user=db.Column(db.String(30))
    mspm_create_date=db.Column(db.Date())
    mspm_update_user=db.Column(db.String(30))
    mspm_update_date=db.Column(db.Date())

    payment_method=db.relationship("SoldTransactionHead", backref='payment_method')
    payment_method_purchased_product=db.relationship("PurchasedTransactionHead", backref="payment_method")

class PaymentMethodSchema(Schema):
    """Schema to retrieve data from Model Stock as dictionary.
    data_key is an alias for column name"""
    mspm_id=fields.Int(data_key='payment_method_id')
    mspm_desc=fields.Str(data_key='payment_method')
    mspm_active_status=fields.Str(data_key='active_status')