from flask import jsonify
from .discountModel import db,Discount, DiscountSchema

class DiscountController:
    def insert(self):
        data=Discount(msd_id=1, msd_msdt_id=1, msd_desc='Promo 11.11', msd_nominal=50,msd_status_aktif='Y' )
        db.session.add(data)
        db.session.commit()
        return 'sukses'
        
    def select(self):
        data=Discount.query.all()
        result=DiscountSchema(many=True).dump(data)
        return jsonify(result)
    
