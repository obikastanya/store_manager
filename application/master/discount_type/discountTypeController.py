from flask import jsonify
from .discountTypeModel import db,DiscountType, DiscountTypeSchema

class DiscountTypeController:
    def insert(self):
        data=DiscountType(msdt_id=1, msdt_desc='Promo 11.11', msdt_status_aktif='Y')
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=DiscountType.query.all()
        result=DiscountTypeSchema(many=True).dump(data)
        return jsonify(result)
    
