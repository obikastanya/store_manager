from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from app import db


class SoldTransactionHead(db.Model):
    __tablename__='transaction_sold_head'
    th_id=db.Column(db.Integer(), primary_key=True)
    th_mspm_id=db.Column(db.Integer(), db.ForeignKey('ms_payment_method.mspm_id'))
    th_mse_id=db.Column(db.Integer(),db.ForeignKey('ms_employee.mse_id'))
    th_total_price=db.Column(postgresql.NUMERIC(12,2))
    th_paid=db.Column(postgresql.NUMERIC(12,2))
    th_change=db.Column(postgresql.NUMERIC(12,2))
    th_tax=db.Column(postgresql.NUMERIC(12,2))
    th_date=db.Column(db.Date())
    # use back populates so head can access detail and also the other verse
    detail_transaction=relationship('SoldTransactionDetail',back_populates='sold_transaction')

 
class SoldTransactionDetail(db.Model):
    __tablename__='transaction_sold_detail'
    td_id=db.Column(db.Integer(),primary_key=True)
    td_th_id=db.Column(db.Integer(),db.ForeignKey('transaction_sold_head.th_id'))
    td_msp_id=db.Column(db.Integer(),db.ForeignKey('ms_product.msp_id'))
    td_quantity=db.Column(db.Integer())
    td_on_sale_price=db.Column(postgresql.NUMERIC(12,2))

    sold_transaction=relationship('SoldTransactionHead',back_populates='detail_transaction')
    detail_discount_applied=relationship('SoldTransactionDetailDiscountApplied',back_populates='detail_transaction')
 
class SoldTransactionDetailDiscountApplied(db.Model):
    __tablename__='transaction_sold_discount_applied'
    tdda_id=db.Column(db.Integer(),primary_key=True)
    tdda_td_id=db.Column(db.Integer(), db.ForeignKey('transaction_sold_detail.td_id'))
    tdda_msdt_id=db.Column(db.Integer(),db.ForeignKey('ms_discount_type.msdt_id'))
    tdda_cutt_off_nominal=db.Column(postgresql.NUMERIC(12,2))

    detail_discount_applied=relationship('SoldTransactionDetail',back_populates='detail_transaction')


class SoldTransactionHeadSchema(Schema):
    pass

class SoldTransactionDetailSchema(Schema):
    pass

class SoldTransactionDetailDiscountAppliedSchema(Schema):
    pass
 