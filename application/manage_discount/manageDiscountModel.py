from marshmallow import fields, Schema
from app import db


class ManageDiscount(db.Model):
    __tablename__ = 'discount_applied'
    # comma after db.PrimaryKeyConstraint is required, its a shorthand of tupple.
    __table_args__ = (db.PrimaryKeyConstraint('da_msp_id', 'da_msd_id'), )
    da_msp_id = db.Column(db.Integer(), db.ForeignKey('ms_product.msp_id'))
    da_msd_id = db.Column(db.Integer(), db.ForeignKey('ms_discount.msd_id'))
    da_start_date = db.Column(db.Date())
    da_expired_date = db.Column(db.Date())
    da_active_status = db.Column(db.String(1))
    da_create_user = db.Column(db.String(30))
    da_create_date = db.Column(db.Date())
    da_update_user = db.Column(db.String(30))
    da_update_date = db.Column(db.Date())


class ManageDiscountSchema(Schema):
    da_active_status = fields.Str(data_key='active_status')
    da_start_date = fields.Date(data_key='start_date')
    da_expired_date = fields.Date(data_key='expired_date')
    discount_product = fields.Nested("ProductSchema",
                                     only=('msp_id', 'msp_desc'))
    discount_master = fields.Nested('DiscountSchema',
                                    only=('msd_id', 'msd_desc',
                                          'discount_type'))
