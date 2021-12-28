from marshmallow import fields, Schema
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from app import db


class SoldTransactionHead():
    pass 
 
class SoldTransactionDetail():
    pass
 
class SoldTransactionDetailDiscountApplied():
    pass

class SoldTransactionHeadSchema(Schema):
    pass

class SoldTransactionDetailSchema(Schema):
    pass

class SoldTransactionDetailDiscountAppliedSchema(Schema):
    pass
 