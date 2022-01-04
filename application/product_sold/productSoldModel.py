from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
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
    detail_transaction=db.relationship('SoldTransactionDetail',back_populates='sold_transaction', cascade="all, delete, delete-orphan")

 
class SoldTransactionDetail(db.Model):
    __tablename__='transaction_sold_detail'
    td_id=db.Column(db.Integer(),primary_key=True)
    td_th_id=db.Column(db.Integer(),db.ForeignKey('transaction_sold_head.th_id'))
    td_msp_id=db.Column(db.Integer(),db.ForeignKey('ms_product.msp_id'))
    td_quantity=db.Column(db.Integer())
    td_on_sale_price=db.Column(postgresql.NUMERIC(12,2))

    sold_transaction=db.relationship('SoldTransactionHead',back_populates='detail_transaction')
    detail_discount_applied=db.relationship('SoldTransactionDetailDiscountApplied',back_populates='detail_transaction',cascade="all, delete, delete-orphan")
 
class SoldTransactionDetailDiscountApplied(db.Model):
    __tablename__='transaction_sold_discount_applied'
    __table_args__=(db.ForeignKeyConstraint(["tdda_da_product_id","tdda_da_discount_id"],["discount_applied.da_msp_id","discount_applied.da_msd_id"]),)
    tdda_id=db.Column(db.Integer(),primary_key=True)
    tdda_td_id=db.Column(db.Integer(), db.ForeignKey('transaction_sold_detail.td_id'))
    tdda_msdt_id=db.Column(db.Integer(),db.ForeignKey('ms_discount_type.msdt_id'))
    tdda_da_product_id=db.Column(db.Integer())
    tdda_da_discount_id=db.Column(db.Integer())
    tdda_cutt_off_nominal=db.Column(postgresql.NUMERIC(12,2))

    detail_transaction=db.relationship('SoldTransactionDetail',back_populates='detail_discount_applied')


class SoldTransactionHeadSchema(Schema):
    th_id=fields.Int(data_key='transaction_id')
    th_total_price=fields.Int(data_key="total_price")
    th_paid=fields.Int(data_key="paid")
    th_change=fields.Int(data_key="change")
    th_tax=fields.Int(data_key="tax")
    th_date=fields.Date(data_key="transaction_date")
    payment_method=fields.Nested("PaymentMethodSchema",only=("mspm_id","mspm_desc"))
    employee_transaction=fields.Nested("EmployeeSchema",only=("mse_id","mse_name"))
    detail_transaction=fields.List(fields.Nested("SoldTransactionDetailSchema"))
    detail_discount_applied=fields.Nested('SoldTransactionDetailDiscountAppliedSchema')

class SoldTransactionDetailSchema(Schema):
    td_id=fields.Int(data_key='detail_transaction_id')
    product=fields.Nested("ProductSchema",only=("msp_id","msp_desc"))
    td_quantity=fields.Int(data_key="quantity")
    td_on_sale_price=fields.Int(data_key='saled_price')
    detail_discount_applied=fields.List(fields.Nested("SoldTransactionDetailDiscountAppliedSchema"))

class SoldTransactionDetailDiscountAppliedSchema(Schema):
    tdda_id=fields.Int(data_key='transaction_discount_applied_id')
    tdda_cutt_off_nominal=fields.Int(data_key='cutt_off_nominal')
    discount_applied=fields.Nested("ManageDiscountSchema", only=("discount_master",))
 