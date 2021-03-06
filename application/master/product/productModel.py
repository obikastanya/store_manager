from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref
from app import db
from application.master.category_product.categoryProductModel import CategoryProduct


class Product(db.Model):
    """Object for table ms_product"""
    __tablename__ = 'ms_product'
    msp_id = db.Column(db.Integer(), primary_key=True)
    msp_brand = db.Column(db.String(100))
    msp_msc_id = db.Column(db.Integer(), db.ForeignKey('ms_category.msc_id'))
    msp_price = db.Column(postgresql.NUMERIC(12))
    msp_desc = db.Column(db.String(500))
    msp_mssp_id = db.Column(db.Integer(), db.ForeignKey('ms_supplier.mssp_id'))
    msp_mscp_id = db.Column(db.Integer(), db.ForeignKey('ms_company.mscp_id'))
    msp_active_status = db.Column(db.String(1))
    msp_create_user = db.Column(db.String(30))
    msp_create_date = db.Column(db.Date())
    msp_update_user = db.Column(db.String(30))
    msp_update_date = db.Column(db.Date())
    # relationship
    stock = db.relationship('Stock',
                              back_populates='product', uselist=False)
    discount_applied_on_product = db.relationship('ManageDiscount',
                                       back_populates="discount_product")
    product_saled=db.relationship('SoldTransactionDetail',backref='product')
    product_for_purchased_transaction_detail=db.relationship('PurchasedTransactionDetail',backref='product')


class ProductSchema(Schema):
    """Schema to retrieve data from Model Product as dictionary.
    data_key is an alias for column name"""
    msp_id = fields.Int(data_key='product_id')
    msp_brand = fields.Str(data_key='brand')
    msp_price = fields.Int(data_key='price')
    msp_desc = fields.Str(data_key='product_desc')
    msp_active_status = fields.Str(data_key='active_status')
    category_product = fields.Nested('CategoryProductSchema',
                                     only=('msc_id', 'msc_desc'))
    supplier = fields.Nested('SupplierSchema', only=('mssp_id', 'mssp_desc'))
    company = fields.Nested('CompanySchema', only=('mscp_id', 'mscp_desc'))
    discount_applied_on_product=fields.List( fields.Nested('ManageDiscountSchema', only=('da_expired_date','da_start_date','da_active_status','discount_master')))
    stock=fields.Nested('StockSchema',only=('mss_id','mss_store_stock','mss_warehouse_stock'))
