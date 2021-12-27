from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import schema
from sqlalchemy.sql.schema import ForeignKey
from app import db
from ..discount_type.discountTypeModel import DiscountTypeSchema


class Discount(db.Model):
    __tablename__ = 'ms_discount'
    msd_id = db.Column(db.Integer(), primary_key=True)
    msd_msdt_id = db.Column(db.Integer(),
                            db.ForeignKey('ms_discount_type.msdt_id'))
    msd_desc = db.Column(db.String(150))
    msd_nominal = db.Column(postgresql.NUMERIC(12))
    msd_active_status = db.Column(db.String(1))
    msd_create_user = db.Column(db.String(30))
    msd_create_date = db.Column(db.Date())
    msd_update_user = db.Column(db.String(30))
    msd_update_date = db.Column(db.Date())

    discount_master = db.relationship('ManageDiscount',
                                      backref='discount_master')


class DiscountSchema(Schema):
    msd_id = fields.Int(data_key='discount_id')
    msd_desc = fields.Str(data_key='desc')
    msd_nominal = fields.Int(data_key='discount_nominal')
    msd_active_status = fields.Str(data_key='active_status')
    discount_type = fields.Nested('DiscountTypeSchema',
                                  only=('msdt_id', 'msdt_desc'))
