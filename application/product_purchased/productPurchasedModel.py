from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from app import db


class PurchasedTransactionHead(db.Model):
    __tablename__='transaction_purchased_head'
    tp_id=db.Column(db.Integer(), primary_key=True)
    tp_mssp_id=db.Column(db.Integer(), db.ForeignKey('ms_supplier.mssp_id'))
    tp_mspm_id=db.Column(db.Integer(), db.ForeignKey('ms_payment_method.mspm_id'))
    tp_nominal=db.Column(postgresql.NUMERIC(12,2))
    tp_date=db.Column(db.Date())
    # use back populates so head can access detail and also the other verse
    detail_transaction=db.relationship('PurchasedTransactionDetail',back_populates='purchased_transaction', cascade="all, delete, delete-orphan")

 
class PurchasedTransactionDetail(db.Model):
    __tablename__='transaction_purchased_detail'
    tpd_id=db.Column(db.Integer(),primary_key=True)
    tpd_tp_id=db.Column(db.Integer(),db.ForeignKey('transaction_purchased_head.tp_id'))
    tpd_msp_id=db.Column(db.Integer(),db.ForeignKey('ms_product.msp_id'))
    tpd_msp_price=db.Column(postgresql.NUMERIC(12,2))
    tpd_quantity=db.Column(postgresql.NUMERIC(12,2))

    purchased_transaction=db.relationship('PurchasedTransactionHead',back_populates='detail_transaction')

class PurchasedTransactionHeadSchema(Schema):
    tp_id=fields.Int(data_key='purchased_transaction_id')
    supplier=fields.Nested('SupplierSchema', only=('mssp_id','mssp_desc',))
    payment_method=fields.Nested('PaymentMethodSchema',only=('mspm_id','mspm_desc',))
    tp_nominal=fields.Int(data_key='nominal')
    tp_date=fields.Date(data_key='purchasing_date')
    
    detail_transaction=fields.List(fields.Nested('PurchasedTransactionDetailSchema'))

class PurchasedTransactionDetailSchema(Schema):
    tpd_id=fields.Int(data_key='transaction_purchased_detail_id')
    product=fields.Nested('ProductSchema',only=('msp_id', 'msp_desc',))
    tpd_msp_price=fields.Int(data_key='purchased_price')
    td_quantity=fields.Int(data_key='quantity')